from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.contrib.auth import get_user_model
import uuid

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
    
    


User = get_user_model()

class PasswordResetOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    token = models.UUIDField(default=uuid.uuid4, editable=False)

    def is_valid(self):
        # OTP valid for 5 minutes
        return (timezone.now() - self.created_at).total_seconds() < 300 and not self.is_used

    def __str__(self):
        return f"OTP for {self.user.username}"
