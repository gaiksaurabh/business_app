from django.contrib import admin
from .models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'job_details', 'job_size', 'received')

    def received(self, obj):
        # Example: return Yes/No depending on some condition
        return "Yes" if obj.status == "Received" else "No"
