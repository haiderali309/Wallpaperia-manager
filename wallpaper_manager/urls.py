from django.contrib import admin
from django.urls import path
from wallpapers import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Category Management
    path('categories/', views.manage_categories, name='manage_categories'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/edit/<str:category_id>/', views.edit_category, name='edit_category'),
    path('categories/delete/<str:category_id>/', views.delete_category, name='delete_category'),
    
    # Category Wallpapers
    path('categories/<str:category_id>/wallpapers/', views.category_wallpapers, name='category_wallpapers'),
    path('categories/<str:category_id>/wallpapers/add/', views.add_wallpaper_to_category, name='add_wallpaper_to_category'),
    path('categories/<str:category_id>/wallpapers/remove/<int:index>/', views.remove_wallpaper_from_category, name='remove_wallpaper_from_category'),
    
    # Static Categories - CHANGED FROM /static/ to /category/
    path('category/<str:category_name>/', views.static_category_view, name='static_category'),
    path('category/<str:category_name>/add/', views.add_wallpaper_to_static, name='add_wallpaper_to_static'),
    path('category/<str:category_name>/remove/<int:index>/', views.remove_wallpaper_from_static, name='remove_wallpaper_from_static'),
    
    # User Management
    path('users/', views.manage_users, name='manage_users'),
    path('users/add/', views.add_user, name='add_user'),
    path('users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),


    path('superuser/forgot-password/', views.superuser_forgot_password, name='superuser_forgot_password'),
    path('superuser/verify-otp/', views.superuser_verify_otp, name='superuser_verify_otp'),
    path('superuser/reset-password/', views.superuser_reset_password, name='superuser_reset_password'),


    ]