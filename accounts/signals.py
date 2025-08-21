from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from .models import CustomerProfile

@receiver(post_save, sender=CustomerProfile)
def generate_customer_id(sender, instance, created, **kwargs):
    if created and not instance.customer_id:
        def set_customer_id():
            last_profile = CustomerProfile.objects.exclude(customer_id__isnull=True).order_by("-id").first()
            if last_profile and last_profile.customer_id.startswith("AOP"):
                last_number = int(last_profile.customer_id.replace("AOP", ""))
                new_number = last_number + 1
            else:
                new_number = 1
            instance.customer_id = f"AOP{new_number:04d}"
            instance.save(update_fields=["customer_id"])
        transaction.on_commit(set_customer_id)
