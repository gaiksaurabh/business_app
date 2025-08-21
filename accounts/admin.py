from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Profile, CustomerProfile, DeletedUser

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Account Profile'
    fk_name = 'user'
    fields = ['whatsapp_number', 'press_name', 'raw_password']

class CustomerProfileInline(admin.StackedInline):
    model = CustomerProfile
    can_delete = False
    verbose_name_plural = 'Customer Profile'
    fk_name = 'user'
    fields = ['customer_id', 'whatsapp_number']

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, CustomerProfileInline)
    list_display = ('username', 'email', 'first_name', 'last_name', 
                   'is_staff', 'is_superuser', 'get_raw_password', 'get_whatsapp_number', 'get_press_name', 'is_deleted', 'deleted_at')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_deleted', 'groups')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', 'deleted_at')}),
        (_('Status'), {'fields': ('is_deleted',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name'),
        }),
    )
    
    readonly_fields = ('deleted_at', 'last_login', 'date_joined')
    
    def get_inline_instances(self, request, obj=None):
        # Only show inlines when editing an existing object
        if not obj:
            return []
        return super().get_inline_instances(request, obj)

    def get_raw_password(self, obj):
        if hasattr(obj, 'account_profile') and obj.account_profile:
            return obj.account_profile.raw_password
        elif hasattr(obj, 'customer_profile') and obj.customer_profile:
            return obj.customer_profile.raw_password
        return "-"
    get_raw_password.short_description = 'Password'

    def get_whatsapp_number(self, obj):
        if hasattr(obj, 'account_profile') and obj.account_profile:
            return obj.account_profile.whatsapp_number
        elif hasattr(obj, 'customer_profile') and obj.customer_profile:
            return obj.customer_profile.whatsapp_number
        return "-"
    get_whatsapp_number.short_description = 'WhatsApp'

    def get_press_name(self, obj):
        if hasattr(obj, 'account_profile') and obj.account_profile:
            return obj.account_profile.press_name
        elif hasattr(obj, 'customer_profile') and obj.customer_profile:
            return obj.customer_profile.press_name
        return "-"
    get_press_name.short_description = 'Press Name'


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'whatsapp_number', 'press_name', 'raw_password']
    list_filter = ['press_name']
    search_fields = ['user__username', 'user__email', 'whatsapp_number', 'press_name']
    readonly_fields = ['user']

@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'customer_id', 'whatsapp_number']
    list_filter = ['customer_id']
    search_fields = ['user__username', 'user__email', 'customer_id', 'whatsapp_number']
    readonly_fields = ['user']

@admin.register(DeletedUser)
class DeletedUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role', 'deleted_at', 'deleted_reason']
    list_filter = ['deleted_at', 'role']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'deleted_reason']
    readonly_fields = [
        'original_id', 'username', 'email', 'first_name', 
        'last_name', 'date_joined', 'deleted_at', 'unique_deleted_id'
    ]
    
    fieldsets = (
        (_('User Information'), {
            'fields': ('original_id', 'username', 'email', 'first_name', 'last_name')
        }),
        (_('Deletion Details'), {
            'fields': ('date_joined', 'deleted_at', 'deleted_reason', 'unique_deleted_id')
        }),
        (_('Role Information'), {
            'fields': ('role',)
        }),
    )
    
    def has_add_permission(self, request):
        # Prevent adding deleted users manually
        return False
    
    def has_change_permission(self, request, obj=None):
        # Prevent editing deleted users
        return False

# Register the custom User admin
admin.site.register(User, CustomUserAdmin)