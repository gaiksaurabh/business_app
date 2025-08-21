from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path("admin/", admin.site.urls),

    # Accounts (login/logout, dashboards)
    path("accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),

    # Jobs
    path("jobs/", include("jobs.urls")),

    # Root URL → redirect to login
    path("", lambda request: redirect("accounts:login")),
]

# Serve media & static in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)