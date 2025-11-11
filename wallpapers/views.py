from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import JsonResponse
from .firebase_service import FirebaseService
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password
from .models import PasswordResetOTP
from django.conf import settings

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
import random



User = get_user_model()

STATIC_CATEGORIES = ['Animated', 'Art', 'Black & White', 'Feature', 'Horror', 'Nature', 'Sports', 'Tech']

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    categories = FirebaseService.get_categories()
    static_cats = {cat: FirebaseService.get_static_category(cat) for cat in STATIC_CATEGORIES}
    return render(request, 'dashboard.html', {
        'categories': categories,
        'static_categories': static_cats,
        'static_names': STATIC_CATEGORIES
    })

@login_required
def manage_categories(request):
    if not request.user.can_edit():
        messages.error(request, 'Permission denied')
        return redirect('dashboard')
    
    categories = FirebaseService.get_categories()
    return render(request, 'manage_categories.html', {'categories': categories})

@login_required
def add_category(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        name = request.POST.get('name')
        c_url = request.POST.get('c_url')
        
        FirebaseService.add_category(category_id, name, c_url)
        messages.success(request, 'Category added successfully')
        return redirect('manage_categories')
    
    return render(request, 'add_category.html')

@login_required
def edit_category(request, category_id):
    if request.method == 'POST':
        name = request.POST.get('name')
        c_url = request.POST.get('c_url')
        
        FirebaseService.update_category(category_id, name, c_url)
        messages.success(request, 'Category updated successfully')
        return redirect('manage_categories')
    
    categories = FirebaseService.get_categories()
    category = categories.get(category_id, {})
    return render(request, 'edit_category.html', {
        'category_id': category_id,
        'category': category
    })

@login_required
def delete_category(request, category_id):
    if not request.user.can_delete():
        messages.error(request, 'Permission denied')
        return redirect('manage_categories')
    
    FirebaseService.delete_category(category_id)
    messages.success(request, 'Category deleted successfully')
    return redirect('manage_categories')

@login_required
def category_wallpapers(request, category_id):
    categories = FirebaseService.get_categories()
    category = categories.get(category_id, {})
    wallpapers = category.get('wallpapers', [])
    
    return render(request, 'category_wallpapers.html', {
        'category_id': category_id,
        'category': category,
        'wallpapers': wallpapers
    })

@login_required
def add_wallpaper_to_category(request, category_id):
    if request.method == 'POST':
        wallpaper_url = request.POST.get('wallpaper_url')
        FirebaseService.add_wallpaper_to_category(category_id, wallpaper_url)
        messages.success(request, 'Wallpaper added successfully')
        return redirect('category_wallpapers', category_id=category_id)
    
    return render(request, 'add_wallpaper.html', {'category_id': category_id})

@login_required
def remove_wallpaper_from_category(request, category_id, index):
    if not request.user.can_delete():
        messages.error(request, 'Permission denied')
        return redirect('category_wallpapers', category_id=category_id)
    categories = FirebaseService.get_categories()
    category = categories.get(category_id, {})
    wallpapers = category.get('wallpapers', [])
    
    if 0 <= index < len(wallpapers):
        wallpaper_url = wallpapers[index]
        FirebaseService.remove_wallpaper_from_category(category_id, wallpaper_url)
        messages.success(request, 'Wallpaper removed successfully')
    
    return redirect('category_wallpapers', category_id=category_id)

@login_required
def static_category_view(request, category_name):
    wallpapers = FirebaseService.get_static_category(category_name)
    return render(request, 'static_category.html', {
        'category_name': category_name,
        'wallpapers': wallpapers
    })

@login_required
def add_wallpaper_to_static(request, category_name):
    if request.method == 'POST':
        wallpaper_url = request.POST.get('wallpaper_url')
        FirebaseService.add_wallpaper_to_static(category_name, wallpaper_url)
        messages.success(request, 'Wallpaper added successfully')
        return redirect('static_category', category_name=category_name)
    
    return render(request, 'add_wallpaper_static.html', {'category_name': category_name})

@login_required
def remove_wallpaper_from_static(request, category_name, index):
    wallpapers = FirebaseService.get_static_category(category_name)
    if 0 <= index < len(wallpapers):
        wallpaper_url = wallpapers[index]
        FirebaseService.remove_wallpaper_from_static(category_name, wallpaper_url)
        messages.success(request, 'Wallpaper removed successfully')
    
    return redirect('static_category', category_name=category_name)

@login_required
def manage_users(request):
    if request.user.role != 'superuser':
        messages.error(request, 'Only superusers can manage users')
        return redirect('dashboard')
    
    users = User.objects.all()
    return render(request, 'manage_users.html', {'users': users})

@login_required
def add_user(request):
    if request.user.role != 'superuser':
        messages.error(request, 'Permission denied')
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')
        
        user = User.objects.create_user(username=username, password=password)
        user.role = role
        user.save()
        messages.success(request, 'User created successfully')
        return redirect('manage_users')
    
    return render(request, 'add_user.html')


from django.contrib.auth.hashers import make_password

@login_required
def edit_user(request, user_id):
    if request.user.role not in ['superuser', 'admin']:
        messages.error(request, 'Permission denied.')
        return redirect('manage_users')

    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')

        user.username = username
        user.role = role

        if password:  # Only update password if provided
            user.password = make_password(password)

        user.save()
        messages.success(request, f"User '{user.username}' updated successfully.")
        return redirect('manage_users')

    return render(request, 'edit_user.html', {'user': user})



@login_required
def delete_user(request, user_id):
    if request.user.role not in ['superuser', 'admin']:
        messages.error(request, 'Permission denied.')
        return redirect('manage_users')

    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        if user.username == request.user.username:
            messages.error(request, "You cannot delete yourself.")
        elif user.role == 'superuser' and request.user.role != 'superuser':
            messages.error(request, "Only superusers can delete another superuser.")
        else:
            user.delete()
            messages.success(request, f"User '{user.username}' deleted successfully.")
        return redirect('manage_users')

    return render(request, 'delete_user.html', {'user': user})


# Step 1: Request email and send OTP
def superuser_forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email, is_superuser=True)
        except User.DoesNotExist:
            messages.error(request, "No superuser found with that email.")
            return redirect('superuser_forgot_password')

        otp = str(random.randint(100000, 999999))
        request.session['otp'] = otp
        request.session['email'] = email

        send_mail(
            subject='Your Superuser Password Reset OTP',
            message=f'Your OTP for password reset is: {otp}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )

        messages.success(request, "OTP sent to your registered email.")
        return redirect('superuser_verify_otp')

    return render(request, 'superuser_forgot_password.html')


# Step 2: Verify OTP
def superuser_verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        stored_otp = request.session.get('otp')

        if entered_otp == stored_otp:
            return redirect('superuser_reset_password')
        else:
            messages.error(request, "Invalid OTP. Try again.")
            return redirect('superuser_verify_otp')

    return render(request, 'superuser_verify_otp.html')


# Step 3: Reset Password
def superuser_reset_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('password')
        email = request.session.get('email')

        try:
            user = User.objects.get(email=email, is_superuser=True)
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password reset successfully!")
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, "Error resetting password.")
            return redirect('superuser_forgot_password')

    return render(request, 'superuser_reset_password.html')


def superuser_required(view_func):
    decorated_view_func = user_passes_test(
        lambda u: u.is_superuser,
        login_url='/login/'
    )(view_func)
    return decorated_view_func


@superuser_required
def superuser_password_reset(request):
    return render(request, 'superuser_password_reset.html')