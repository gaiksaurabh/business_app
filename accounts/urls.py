# accounts/urls.py

from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("dashboard/", views.dashboard_home, name="dashboard"),
    path("dashboard-home/", views.dashboard_home, name="dashboard_home"),
    path("all-users/", views.all_users, name="all_users"),

    # User management
    path("add-user/", views.add_user, name="add_user"),
    path("edit/<int:user_id>/", views.edit_user, name="edit_user"),
    path("delete/<int:user_id>/", views.delete_user, name="delete_user"),
    path("restore/<int:deleted_id>/", views.restore_user, name="restore_user"),

    # Recycle bin
    path("recycle-bin/", views.recycle_bin, name="recycle_bin"),
    path('user/<int:deleted_user_id>/permanent-delete/', views.permanent_delete_user, name='permanent_delete_user'),

    # Import/export
    path("upload-users/", views.upload_users, name="upload_users"),
    path("download-excel/", views.download_excel, name="download_excel"),
    path("download-pdf/", views.download_pdf, name="download_pdf"),

    # Authentication
    path("login/", views.custom_login, name="login"),
    path("logout/", views.custom_logout, name="custom_logout"),

    path('send-whatsapp/<int:user_id>/', views.send_whatsapp_welcome, name='send_whatsapp_welcome'),
]