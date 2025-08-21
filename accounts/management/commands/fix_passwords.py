from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import Profile
import random
import string

User = get_user_model()

class Command(BaseCommand):
    help = 'Fix passwords for existing users by generating new ones'

    def handle(self, *args, **options):
        users = User.objects.all()
        
        for user in users:
            # Generate a new password
            chars = string.ascii_letters + string.digits + "!@#$%^&*"
            raw_password = ''.join(random.choice(chars) for _ in range(12))
            
            # Set the password (this hashes it)
            user.set_password(raw_password)
            user.save()
            
            # Store the raw password in profile
            profile, created = Profile.objects.get_or_create(user=user)
            profile.raw_password = raw_password
            
            # Get login link
            from django.contrib.sites.models import Site
            current_site = Site.objects.get_current()
            profile.login_link = f"http://{current_site.domain}/accounts/login/"
            
            profile.save()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f"Fixed password for {user.username}: {raw_password}"
                )
            )