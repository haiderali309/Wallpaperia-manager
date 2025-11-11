# 🖼️ Django Wallpaper Manager - Complete Documentation

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Technology Stack](#technology-stack)
4. [Installation & Setup](#installation--setup)
5. [Database Configuration](#database-configuration)
6. [User Management System](#user-management-system)
7. [Password Reset System](#password-reset-system)
8. [Firebase Integration](#firebase-integration)
9. [Project Structure](#project-structure)
10. [API Reference](#api-reference)
11. [Deployment Guide](#deployment-guide)

---

## 🎯 Project Overview

A production-ready Django application for managing wallpaper collections stored in Firebase Realtime Database. Features include role-based access control, dynamic category management, OTP-based password recovery, and a beautiful responsive UI.

---

## ✨ Features

### 🔐 Authentication & Authorization
- **Role-Based Access Control (RBAC)**
  - **Super User**: Full system access + user management
  - **Admin**: Can add/edit/delete wallpapers and categories
  - **Editor**: Can only add/update (no delete permissions)
- **Secure Password Reset with OTP**
  - Email-based OTP verification
  - 5-minute OTP expiry
  - One-time use tokens
  - Only for superusers

### 📁 Category Management
- **Static Categories**: Pre-defined categories (Animated, Art, Black & White, Feature, Horror, Nature, Sports, Tech)
- **Dynamic Categories**: User-created categories with custom names and cover images
- Full CRUD operations on categories (role-dependent)

### 🖼️ Wallpaper Management
- Add wallpapers via URL
- Real-time image preview
- Grid-based display with lazy loading
- Bulk operations support
- Automatic fallback for broken images

### 🎨 UI/UX
- Modern gradient design
- Responsive grid layout
- Smooth animations and transitions
- Professional card-based interface
- Mobile-friendly design

---

## 🛠️ Technology Stack

### Backend
- **Django 5.0** - Web framework
- **PostgreSQL** - Production database
- **Firebase Realtime Database** - Wallpaper storage
- **Python 3.8+**

### Frontend
- **HTML5/CSS3** - Structure and styling
- **JavaScript** - Interactive features
- **Django Templates** - Server-side rendering

### Additional Libraries
- **firebase-admin** - Firebase integration
- **python-decouple** - Environment configuration
- **whitenoise** - Static file serving
- **gunicorn** - WSGI HTTP server
- **pillow** - Image processing

---

## 📦 Installation & Setup

### 1. Clone or Create Project

```bash
# Create project directory
mkdir wallpaper_manager
cd wallpaper_manager

# Create Django project
django-admin startproject wallpaper_manager .
python manage.py startapp wallpapers
```

### 2. Install Dependencies

```bash
pip install django==5.0
pip install firebase-admin
pip install python-decouple
pip install pillow
pip install whitenoise
pip install gunicorn
pip install psycopg2-binary  # PostgreSQL adapter
```

**requirements.txt:**
```txt
Django==5.0
firebase-admin==6.3.0
python-decouple==3.8
pillow==10.1.0
whitenoise==6.6.0
gunicorn==21.2.0
psycopg2-binary==2.9.9
```

### 3. Firebase Setup

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project or select existing
3. Go to **Project Settings → Service Accounts**
4. Click **Generate New Private Key**
5. Download JSON file and save as `firebase_credentials.json` in project root

### 4. Environment Configuration

Create `.env` file in project root:

```env
SECRET_KEY=your-django-secret-key-here
DEBUG=True
FIREBASE_DATABASE_URL=https://your-project.firebaseio.com

# PostgreSQL Configuration
DB_NAME=wallpaper_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# Email Configuration (for OTP)
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```

### 5. Create Required Directories

```bash
mkdir templates
mkdir static
mkdir staticfiles
mkdir media
mkdir wallpapers/management
mkdir wallpapers/management/commands
mkdir wallpapers/templatetags
```

### 6. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser

```bash
python manage.py createsuperuser
```

Then set role to superuser:
```bash
python manage.py shell
```
```python
from wallpapers.models import User
user = User.objects.get(username='your_username')
user.role = 'superuser'
user.save()
exit()
```

### 8. Start Development Server

```bash
python manage.py runserver
```

Access at: `http://127.0.0.1:8000`

---

## 🗄️ Database Configuration

### PostgreSQL Setup

#### Option 1: Local PostgreSQL

1. **Install PostgreSQL**
   ```bash
   # Windows: Download from postgresql.org
   # Mac: brew install postgresql
   # Linux: sudo apt-get install postgresql
   ```

2. **Create Database**
   ```sql
   CREATE DATABASE wallpaper_db;
   CREATE USER wallpaper_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE wallpaper_db TO wallpaper_user;
   ```

3. **Update settings.py**
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': config('DB_NAME', default='wallpaper_db'),
           'USER': config('DB_USER', default='postgres'),
           'PASSWORD': config('DB_PASSWORD'),
           'HOST': config('DB_HOST', default='localhost'),
           'PORT': config('DB_PORT', default='5432'),
       }
   }
   ```

#### Option 2: SQLite (Development Only)

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

---

## 👥 User Management System

### 1️⃣ User Model

Custom user model with role-based permissions:

```python
class User(AbstractUser):
    ROLE_CHOICES = [
        ('superuser', 'Super User'),
        ('admin', 'Admin'),
        ('editor', 'Editor'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='editor')
    
    def can_delete(self):
        return self.role in ['superuser', 'admin']
    
    def can_edit(self):
        return self.role in ['superuser', 'admin', 'editor']
```

**Features:**
- Extends Django's `AbstractUser`
- Custom `role` field for RBAC
- Passwords stored hashed using Django's `set_password()`
- Permission helper methods

### Role Permissions Matrix

| Action | Super User | Admin | Editor |
|--------|-----------|-------|--------|
| View Dashboard | ✅ | ✅ | ✅ |
| Add Wallpapers | ✅ | ✅ | ✅ |
| Update Wallpapers | ✅ | ✅ | ✅ |
| Delete Wallpapers | ✅ | ✅ | ❌ |
| Add Categories | ✅ | ✅ | ✅ |
| Update Categories | ✅ | ✅ | ✅ |
| Delete Categories | ✅ | ✅ | ❌ |
| Manage Users | ✅ | ❌ | ❌ |
| Reset Password (OTP) | ✅ | ❌ | ❌ |

---

## 🔑 Password Reset System

### 2️⃣ OTP Model

Secure OTP storage in PostgreSQL:

```python
class PasswordResetOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    
    def is_valid(self):
        """Check if OTP is valid (5 minutes expiry)"""
        expiry_time = timedelta(minutes=5)
        return (timezone.now() - self.created_at) < expiry_time and not self.is_used
```

**Features:**
- 6-digit OTP codes
- 5-minute expiry
- One-time use flag
- Unique UUID tokens
- ForeignKey relationship to User

### 3️⃣ SMTP Email Setup

Configure in `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')  # App Password
DEFAULT_FROM_EMAIL = config('EMAIL_HOST_USER')
```

**Gmail App Password Setup:**
1. Enable 2-Factor Authentication on Google Account
2. Go to: https://myaccount.google.com/apppasswords
3. Generate app password for "Mail"
4. Use this password in `.env` file

### 4️⃣ Password Reset Flow

**Step 1: Forgot Password**
```
URL: /superuser/forgot-password/
View: superuser_forgot_password
- User enters email
- System validates email belongs to superuser
- Generates 6-digit OTP
- Sends OTP via SMTP
- Stores OTP in database
```

**Step 2: Verify OTP**
```
URL: /superuser/verify-otp/
View: superuser_verify_otp
- User enters OTP
- System validates OTP (checks expiry and usage)
- Marks OTP as used
- Redirects to reset password page
```

**Step 3: Reset Password**
```
URL: /superuser/reset-password/
View: superuser_reset_password
- User enters new password
- System updates password using set_password() (hashed)
- Redirects to login page
```

### 5️⃣ URL Configuration

```python
urlpatterns = [
    # Password Reset URLs
    path('superuser/forgot-password/', views.superuser_forgot_password, name='superuser_forgot_password'),
    path('superuser/verify-otp/', views.superuser_verify_otp, name='superuser_verify_otp'),
    path('superuser/reset-password/', views.superuser_reset_password, name='superuser_reset_password'),
]
```

### 6️⃣ Templates

All templates match login page style:

1. **superuser_forgot_password.html** - Enter email
2. **superuser_verify_otp.html** - Enter OTP
3. **superuser_reset_password.html** - Enter new password

**Design Features:**
- Logo displayed like login page
- Card style with gradient (#667eea)
- Full-width buttons
- Back links for navigation
- Consistent branding

### 7️⃣ Login Page Integration

Added "Forgot Password?" link in `login.html`:

```html
<div style="text-align: center; margin-top: 1rem;">
    <a href="{% url 'superuser_forgot_password' %}" style="color: #667eea;">
        Forgot Password?
    </a>
</div>
```

### 8️⃣ Security Features

✅ **Security Measures:**
- Only superuser emails can trigger OTP flow
- Passwords hashed with Django's PBKDF2 algorithm
- OTP expires in 5 minutes
- One-time use tokens
- CSRF protection on all forms
- Rate limiting can be added for production
- Session-based OTP validation

---

## 🔥 Firebase Integration

### Firebase Service Layer

**File:** `wallpapers/firebase_service.py`

#### Category Operations

```python
# Get all categories
categories = FirebaseService.get_categories()

# Add new category
FirebaseService.add_category('gaming', 'Gaming', 'https://image-url.jpg')

# Update category
FirebaseService.update_category('gaming', 'Gaming HD', 'https://new-url.jpg')

# Delete category
FirebaseService.delete_category('gaming')
```

#### Wallpaper Operations

```python
# Add wallpaper to category
FirebaseService.add_wallpaper_to_category('gaming', 'https://wallpaper-url.jpg')

# Remove wallpaper from category
FirebaseService.remove_wallpaper_from_category('gaming', 'https://wallpaper-url.jpg')

# Get static category wallpapers
wallpapers = FirebaseService.get_static_category('Animated')

# Add to static category
FirebaseService.add_wallpaper_to_static('Animated', 'https://wallpaper-url.jpg')
```

### Firebase Data Structure

```json
{
  "wallpapers": {
    "Animated": [
      "https://wallpaper-url-1.jpg",
      "https://wallpaper-url-2.jpg"
    ],
    "Art": [...],
    "Categories": {
      "gaming": {
        "name": "Gaming",
        "C_url": "https://cover-image.jpg",
        "wallpapers": [
          "https://wallpaper-1.jpg",
          "https://wallpaper-2.jpg"
        ]
      }
    }
  }
}
```

---

## 📁 Project Structure

```
wallpaper_manager/
│
├── wallpaper_manager/          # Project configuration
│   ├── __init__.py
│   ├── settings.py            # Django settings
│   ├── urls.py                # Main URL configuration
│   ├── wsgi.py
│   └── asgi.py
│
├── wallpapers/                 # Main application
│   ├── migrations/            # Database migrations
│   ├── management/            # Custom commands
│   │   └── commands/
│   │       └── createsuperuser.py
│   ├── templatetags/          # Custom template filters
│   │   ├── __init__.py
│   │   └── custom_filters.py
│   ├── __init__.py
│   ├── admin.py              # Admin configuration
│   ├── apps.py
│   ├── models.py             # User & OTP models
│   ├── views.py              # View functions
│   ├── firebase_service.py   # Firebase operations
│   └── tests.py
│
├── templates/                  # HTML templates
│   ├── base.html
│   ├── base_login.html
│   ├── login.html
│   ├── dashboard.html
│   ├── manage_categories.html
│   ├── add_category.html
│   ├── edit_category.html
│   ├── category_wallpapers.html
│   ├── add_wallpaper.html
│   ├── static_category.html
│   ├── add_wallpaper_static.html
│   ├── manage_users.html
│   ├── add_user.html
│   ├── superuser_forgot_password.html
│   ├── superuser_verify_otp.html
│   └── superuser_reset_password.html
│
├── static/                     # Static files (CSS, JS, images)
├── staticfiles/               # Collected static files (production)
├── media/                     # User uploaded files
├── firebase_credentials.json  # Firebase service account key
├── .env                       # Environment variables
├── requirements.txt           # Python dependencies
├── manage.py                  # Django management script
└── README.md                  # This file
```

---

## 🔌 API Reference

### View Functions

#### Authentication Views

```python
# Login
login_view(request)
# POST: username, password

# Logout
logout_view(request)
```

#### Dashboard Views

```python
# Main dashboard
dashboard(request)
# Returns: categories, static_categories
```

#### Category Management Views

```python
# List all categories
manage_categories(request)

# Add new category
add_category(request)
# POST: category_id, name, c_url

# Edit category
edit_category(request, category_id)
# POST: name, c_url

# Delete category
delete_category(request, category_id)
# Requires: Admin or SuperUser role
```

#### Wallpaper Management Views

```python
# View category wallpapers
category_wallpapers(request, category_id)

# Add wallpaper to category
add_wallpaper_to_category(request, category_id)
# POST: wallpaper_url

# Remove wallpaper from category
remove_wallpaper_from_category(request, category_id, index)

# View static category
static_category_view(request, category_name)

# Add to static category
add_wallpaper_to_static(request, category_name)
# POST: wallpaper_url

# Remove from static category
remove_wallpaper_from_static(request, category_name, index)
```

#### User Management Views

```python
# List all users
manage_users(request)
# Requires: SuperUser role

# Add new user
add_user(request)
# POST: username, password, role
# Requires: SuperUser role
```

#### Password Reset Views

```python
# Forgot password
superuser_forgot_password(request)
# POST: email

# Verify OTP
superuser_verify_otp(request)
# POST: otp_code

# Reset password
superuser_reset_password(request)
# POST: new_password, confirm_password
```

---

## 🚀 Deployment Guide

### Production Settings

Update `settings.py` for production:

```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Security Settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

### Static Files Collection

```bash
python manage.py collectstatic --noinput
```

### Database Migration

```bash
python manage.py migrate
```

### Run with Gunicorn

```bash
gunicorn wallpaper_manager.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

### Using Nginx (Recommended)

**nginx.conf:**
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location /static/ {
        alias /path/to/staticfiles/;
    }

    location /media/ {
        alias /path/to/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Environment Variables (Production)

```env
SECRET_KEY=generate-new-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

DB_NAME=wallpaper_db
DB_USER=db_user
DB_PASSWORD=secure_password
DB_HOST=db_host
DB_PORT=5432

FIREBASE_DATABASE_URL=https://your-project.firebaseio.com

EMAIL_HOST_USER=noreply@yourdomain.com
EMAIL_HOST_PASSWORD=secure_app_password
```

### Deployment Checklist

- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up PostgreSQL database
- [ ] Configure Firebase credentials
- [ ] Set up email (SMTP)
- [ ] Collect static files
- [ ] Run migrations
- [ ] Create superuser
- [ ] Configure SSL/HTTPS
- [ ] Set up domain name
- [ ] Configure firewall
- [ ] Set up backup strategy
- [ ] Configure logging
- [ ] Set up monitoring
- [ ] Test all functionality

---

## 📝 Additional Notes

### Custom Management Commands

**Create superuser with role:**
```bash
python manage.py createsuperuser
# Then manually set role in Django shell or admin
```

### Template Tags

**custom_filters.py:**
```python
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
```

**Usage in templates:**
```django
{% load custom_filters %}
{{ static_categories|get_item:cat_name }}
```

### Common Issues & Solutions

**Issue:** Firebase connection error
- **Solution:** Check `firebase_credentials.json` path and permissions

**Issue:** Email not sending
- **Solution:** Verify Gmail app password and enable "Less secure app access"

**Issue:** Static files not loading
- **Solution:** Run `python manage.py collectstatic` and check `STATIC_ROOT`

**Issue:** User role not showing correctly
- **Solution:** Manually set role in Django shell after creating superuser

---

## 📧 Support

For issues and questions:
- Check Django documentation: https://docs.djangoproject.com
- Firebase documentation: https://firebase.google.com/docs
- PostgreSQL documentation: https://www.postgresql.org/docs/

---

## 📄 License

This project is provided as-is for educational and commercial use.

---

📞 Contact & Access
If you want to use this system, contact me:
📧 Email: dev.haider204@gmail.com
I will provide you with the necessary credentials to access and use the system.
Live Link:    https://wallpaperia-manager.onrender.com/

**Last Updated:** November 2025  
**Version:** 1.0.0  
**Django Version:** 5.0  
**Python Version:** 3.8+