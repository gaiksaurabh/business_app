from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import Profile

User = get_user_model()

class Command(BaseCommand):
    help = 'Create missing profiles for existing users'

    def handle(self, *args, **options):
        users_without_profile = User.objects.filter(account_profile__isnull=True)
        
        for user in users_without_profile:
            Profile.objects.get_or_create(user=user)
            self.stdout.write(f'Created profile for {user.username}')
        
        self.stdout.write('Profile creation completed')