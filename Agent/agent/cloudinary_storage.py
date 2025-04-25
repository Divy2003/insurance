import os
from django.conf import settings
from django.utils.deconstruct import deconstructible
from cloudinary_storage.storage import MediaCloudinaryStorage

@deconstructible
class CloudinaryMediaStorage(MediaCloudinaryStorage):
    """
    Django storage backend for Cloudinary.
    
    This class extends the MediaCloudinaryStorage from django-cloudinary-storage
    to provide any custom functionality needed for the insurance application.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def url(self, name):
        """
        Return the URL where the file can be accessed.
        """
        # Use the parent class's url method to get the Cloudinary URL
        return super().url(name)
