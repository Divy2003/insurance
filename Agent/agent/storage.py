import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# Import CloudinaryStorage if available
try:
    from .cloudinary_storage import CloudinaryMediaStorage
    CLOUDINARY_AVAILABLE = True
except ImportError:
    CLOUDINARY_AVAILABLE = False

class MediaStorage:
    """
    Factory class that returns the appropriate storage backend based on settings.
    """
    def __new__(cls, *args, **kwargs):
        # Use Cloudinary storage in production if configured
        if getattr(settings, 'USE_CLOUDINARY_STORAGE', False) and CLOUDINARY_AVAILABLE:
            return CloudinaryMediaStorage()
        else:
            # Otherwise, use the FileSystemStorage
            return FileSystemMediaStorage(*args, **kwargs)

class FileSystemMediaStorage(FileSystemStorage):
    """
    Custom storage backend to handle media files using the file system.
    """
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('location', settings.MEDIA_ROOT)
        kwargs.setdefault('base_url', settings.MEDIA_URL)
        super().__init__(*args, **kwargs)

    def url(self, name):
        """
        Return the URL where the file can be accessed.
        """
        return super().url(name)
