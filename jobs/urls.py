from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="jobs_dashboard"),
]