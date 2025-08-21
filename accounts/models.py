# accounts/models.py

from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
import uuid

# Define choices first
STAFF_TYPES = (
    ("Manager", "Manager"),
    ("Accountant", "Accountant"),
    ("Operator", "Operator"),
    ("Helper", "Helper"),
)

CUSTOMER_TYPES = (
    ("Credit", "Credit"),
    ("Short Credit", "Short Credit"),
    ("Temporary", "Temporary"),
    ("Received", "Received"),
)

# Use your custom User model instead of Django's built-in
class User(AbstractUser):
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    # Fix reverse accessor clashes
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="custom_user_groups",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="custom_user_permissions",
        related_query_name="user",
    )

    def delete(self, using=None, keep_parents=False):
        """Soft delete by default"""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        """Actual database deletion"""
        super().delete()

    class Meta:
        swappable = 'AUTH_USER_MODEL'

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="account_profile"
    )
    whatsapp_number = models.CharField(max_length=20, blank=True, null=True)
    press_name = models.CharField(max_length=100, blank=True, null=True)
    raw_password = models.CharField(max_length=100, blank=True, null=True)
    staff_type = models.CharField(max_length=20, choices=STAFF_TYPES, blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} Profile"

class CustomerProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="customer_profile"
    )
    customer_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    whatsapp_number = models.CharField(max_length=15, blank=True, null=True)
    press_name = models.CharField(max_length=100, blank=True, null=True)
    raw_password = models.CharField(max_length=100, blank=True, null=True)
    customer_type = models.CharField(max_length=20, choices=CUSTOMER_TYPES, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} Customer Profile"

class DeletedUser(models.Model):
    original_id = models.IntegerField(default=0)
    username = models.CharField(max_length=150, default='deleted_user')
    email = models.EmailField(default='deleted@example.com')
    first_name = models.CharField(max_length=30, default='Deleted')
    last_name = models.CharField(max_length=150, default='User')
    whatsapp_number = models.CharField(max_length=20, blank=True, null=True) 
    date_joined = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(auto_now_add=True)
    deleted_reason = models.TextField(blank=True, null=True)
    unique_deleted_id = models.CharField(max_length=50, unique=True, default=uuid.uuid4)
    role = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return f"{self.username} (deleted)"

# Signals
@receiver(post_save, sender=User)
def create_user_profiles(sender, instance, created, **kwargs):
    """
    Ensure every newly created User has a corresponding profile.
    This signal now creates the appropriate profile based on the user's group.
    """
    if created:
        if instance.is_superuser or instance.groups.filter(name="Staff").exists() or instance.groups.filter(name="Admin").exists():
            Profile.objects.get_or_create(user=instance)
        else: # Default to CustomerProfile
            last_profile = CustomerProfile.objects.order_by("-id").first()
            
            if last_profile and last_profile.customer_id:
                try:
                    last_number = int("".join(filter(str.isdigit, last_profile.customer_id)))
                except ValueError:
                    last_number = 0
                new_number = last_number + 1
            else:
                new_number = 1

            customer_id = f"AOP{new_number:04d}"
            CustomerProfile.objects.get_or_create(user=instance, customer_id=customer_id)