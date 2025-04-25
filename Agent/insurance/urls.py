# project/urls.py

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

from agent import views  # Import views from agent app
from agent import admin_views  # Import custom admin views

urlpatterns = [
    path('admin/', admin.site.urls),  # Django's built-in admin
    path('', views.home, name='home'),

    # Custom admin routes
    path('custom-admin/login/', admin_views.admin_login, name='custom_admin_login'),
    path('custom-admin/logout/', admin_views.admin_logout, name='custom_admin_logout'),
    path('custom-admin/dashboard/', admin_views.admin_dashboard, name='custom_admin_dashboard'),

    # Agent management
    path('custom-admin/agent/', admin_views.admin_agent, name='custom_admin_agent'),

    # Posts management
    path('custom-admin/posts/', admin_views.admin_posts_list, name='custom_admin_posts'),
    path('custom-admin/posts/add/', admin_views.admin_post_add, name='custom_admin_post_add'),
    path('custom-admin/posts/<int:post_id>/edit/', admin_views.admin_post_edit, name='custom_admin_post_edit'),
    path('custom-admin/posts/<int:post_id>/delete/', admin_views.admin_post_delete, name='custom_admin_post_delete'),

    # Services management
    path('custom-admin/services/', admin_views.admin_services_list, name='custom_admin_services'),
    path('custom-admin/services/add/', admin_views.admin_service_add, name='custom_admin_service_add'),
    path('custom-admin/services/<int:service_id>/edit/', admin_views.admin_service_edit, name='custom_admin_service_edit'),
    path('custom-admin/services/<int:service_id>/delete/', admin_views.admin_service_delete, name='custom_admin_service_delete'),

    # Optional health check
    path('health/', lambda request: HttpResponse("OK")),
]

# Serve media and static files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# In production, Nginx will handle static and media files
