from django.db import models
from django.utils import timezone
from django.conf import settings

# Import custom storage
from .storage import MediaStorage

# Use custom storage in both development and production
media_storage = MediaStorage()

class Agent(models.Model):
    name = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='agents/', default='default_agent.jpg', storage=media_storage)
    bio = models.TextField(default='')
    phone = models.CharField(max_length=20, default='')
    email = models.EmailField(default='')

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='posts/', storage=media_storage)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class Service(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, help_text="Font Awesome icon class (e.g., 'fa-shield-alt')")
    description = models.TextField(blank=True, null=True, help_text="Optional description of the service")
    order = models.PositiveIntegerField(default=0, help_text="Display order (lower numbers shown first)")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return self.name