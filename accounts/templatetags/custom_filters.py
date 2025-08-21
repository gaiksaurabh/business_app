import re
from django import template

register = template.Library()

@register.filter
def get_profile_field(user, field_name):
    """
    Retrieves a field value from either the user's account_profile or customer_profile.
    Usage: {{ user|get_profile_field:'field_name' }}
    """
    if hasattr(user, 'account_profile') and user.account_profile:
        return getattr(user.account_profile, field_name, None)
    elif hasattr(user, 'customer_profile') and user.customer_profile:
        return getattr(user.customer_profile, field_name, None)
    return None

@register.filter(name="digits_only")
def digits_only(value):
    """
    Removes all non-digit characters from a string (e.g. WhatsApp numbers).
    """
    if not value:
        return ""
    return re.sub(r"\D", "", str(value))