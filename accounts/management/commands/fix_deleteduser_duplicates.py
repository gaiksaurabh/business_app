from django.core.management.base import BaseCommand
from accounts.models import DeletedUser
import uuid

class Command(BaseCommand):
    help = 'Fix duplicate unique_deleted_id values in DeletedUser model'

    def handle(self, *args, **options):
        # Find duplicates
        from django.db.models import Count
        duplicates = DeletedUser.objects.values('unique_deleted_id').annotate(
            count=Count('id')
        ).filter(count__gt=1)
        
        self.stdout.write(f"Found {len(duplicates)} duplicate unique_deleted_id values")
        
        # Fix duplicates
        fixed_count = 0
        for dup in duplicates:
            duplicate_id = dup['unique_deleted_id']
            records = DeletedUser.objects.filter(unique_deleted_id=duplicate_id).order_by('id')
            
            # Keep the first record, update the rest
            for i, record in enumerate(records):
                if i > 0:  # Skip the first record
                    record.unique_deleted_id = str(uuid.uuid4())
                    record.save()
                    fixed_count += 1
                    self.stdout.write(
                        f"Fixed duplicate: {record.username} -> {record.unique_deleted_id}"
                    )
        
        self.stdout.write(
            self.style.SUCCESS(f"Successfully fixed {fixed_count} duplicate records")
        )