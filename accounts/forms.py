# accounts/forms.py

from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
import random, string, secrets
from .models import Profile, CustomerProfile, STAFF_TYPES, CUSTOMER_TYPES

User = get_user_model()

# Helper function to generate passwords, which was in views.py
def generate_password(length=12):
    """Generate a random password with mixed characters"""
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(chars) for _ in range(length))

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class UserCreateForm(forms.ModelForm):
    whatsapp_number = forms.CharField(max_length=20, required=False, label="WhatsApp Number")
    press_name = forms.CharField(max_length=100, required=False, label="Press Name")
    role = forms.ChoiceField(
        choices=[
            ("Customer", "Customer"),
            ("Staff", "Staff"),
            ("Admin", "Admin"),
        ],
        required=True,
        label="Role"
    )
    customer_type = forms.ChoiceField(choices=CUSTOMER_TYPES, required=False, label="Customer Type")
    staff_type = forms.ChoiceField(choices=STAFF_TYPES, required=False, label="Staff Type")

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
    
    def __init__(self, *args, **kwargs):
        # CORRECTED: Call the parent's __init__ method properly
        super().__init__(*args, **kwargs)
        self.fields['first_name'] = forms.CharField(max_length=30, required=True, label="First Name")
        self.fields['last_name'] = forms.CharField(max_length=30, required=True, label="Last Name")
        self.fields['email'] = forms.EmailField(required=True, label="Email")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean_whatsapp_number(self):
        whatsapp = self.cleaned_data.get("whatsapp_number")
        if whatsapp and (Profile.objects.filter(whatsapp_number=whatsapp).exists() or CustomerProfile.objects.filter(whatsapp_number=whatsapp).exists()):
            raise forms.ValidationError("This WhatsApp number is already registered.")
        return whatsapp

    def save(self, commit=True):
        role = self.cleaned_data.get("role")
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        email = self.cleaned_data.get("email")
        whatsapp_number = self.cleaned_data.get("whatsapp_number")
        press_name = self.cleaned_data.get("press_name")
        customer_type = self.cleaned_data.get("customer_type")
        staff_type = self.cleaned_data.get("staff_type")

        prefix = {"Admin": "ADMIN", "Staff": "STAFF", "Customer": "AOP"}[role]
        last_user = User.objects.filter(username__startswith=prefix).order_by("-id").first()
        if last_user:
            digits = "".join(filter(str.isdigit, last_user.username))
            last_number = int(digits) if digits else 0
        else:
            last_number = 0
        
        username = f"{prefix}{str(last_number + 1).zfill(3 if role != 'Customer' else 4)}"
        
        raw_password = generate_password()

        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=raw_password
        )
        
        if role == "Admin":
            user.is_superuser = True
            user.is_staff = True
            user.save()
        else:
            group, _ = Group.objects.get_or_create(name=role)
            user.groups.add(group)
            
        if hasattr(user, 'account_profile') and role != 'Customer':
            profile = user.account_profile
            profile.whatsapp_number = whatsapp_number
            profile.press_name = press_name
            profile.raw_password = raw_password
            profile.staff_type = staff_type
            profile.save()
        elif hasattr(user, 'customer_profile') and role == 'Customer':
            profile = user.customer_profile
            profile.whatsapp_number = whatsapp_number
            profile.press_name = press_name
            profile.raw_password = raw_password
            profile.customer_type = customer_type
            profile.save()

        from django.contrib.sites.models import Site
        current_site = Site.objects.get_current()
        login_link = f"http://{current_site.domain}/accounts/login/"
        
        return user, raw_password, login_link

class UserEditForm(forms.ModelForm):
    whatsapp_number = forms.CharField(max_length=20, required=False, label="WhatsApp Number")
    press_name = forms.CharField(max_length=100, required=False, label="Press Name")
    customer_type = forms.ChoiceField(choices=CUSTOMER_TYPES, required=False, label="Customer Type")
    staff_type = forms.ChoiceField(choices=STAFF_TYPES, required=False, label="Staff Type")

    # Current password field (editable)
    current_password = forms.CharField(
        label='Password',
        widget=forms.TextInput,
        required=False,
        help_text="You can edit the current password."
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username", "current_password"]
        labels = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "email": "Email",
            "username": "Username",
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(self.instance, 'account_profile') and self.instance.account_profile:
            self.fields['whatsapp_number'].initial = self.instance.account_profile.whatsapp_number
            self.fields['press_name'].initial = self.instance.account_profile.press_name
            self.fields['staff_type'].initial = self.instance.account_profile.staff_type
            self.fields['customer_type'].widget = forms.HiddenInput()
            # Set initial value for current password
            self.fields['current_password'].initial = self.instance.account_profile.raw_password
        elif hasattr(self.instance, 'customer_profile') and self.instance.customer_profile:
            self.fields['whatsapp_number'].initial = self.instance.customer_profile.whatsapp_number
            self.fields['press_name'].initial = self.instance.customer_profile.press_name
            self.fields['customer_type'].initial = self.instance.customer_profile.customer_type
            self.fields['staff_type'].widget = forms.HiddenInput()
            # Set initial value for current password
            self.fields['current_password'].initial = self.instance.customer_profile.raw_password

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("This email is already registered.")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        
        # Handle password change
        current_password = self.cleaned_data.get("current_password")
        if current_password:
            user.set_password(current_password)
            if hasattr(user, 'account_profile'):
                user.account_profile.raw_password = current_password
            elif hasattr(user, 'customer_profile'):
                user.customer_profile.raw_password = current_password

        user.save()

        whatsapp_number = self.cleaned_data.get("whatsapp_number")
        press_name = self.cleaned_data.get("press_name")
        customer_type = self.cleaned_data.get("customer_type")
        staff_type = self.cleaned_data.get("staff_type")

        if hasattr(user, "account_profile"):
            user.account_profile.whatsapp_number = whatsapp_number
            user.account_profile.press_name = press_name
            user.account_profile.staff_type = staff_type
            user.account_profile.save()
        elif hasattr(user, "customer_profile"):
            user.customer_profile.whatsapp_number = whatsapp_number
            user.customer_profile.press_name = press_name
            user.customer_profile.customer_type = customer_type
            user.customer_profile.save()
        
        return user