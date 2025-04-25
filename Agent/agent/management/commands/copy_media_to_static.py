import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Copies media files to the static directory for production deployment'

    def handle(self, *args, **kwargs):
        if settings.DEBUG:
            self.stdout.write(self.style.WARNING('This command is intended for production use only.'))
            return

        media_root = settings.MEDIA_ROOT
        static_root = settings.STATIC_ROOT
        
        # Create media directory in static root if it doesn't exist
        static_media_dir = os.path.join(static_root, 'media')
        os.makedirs(static_media_dir, exist_ok=True)
        
        # Copy all files from media directory to static/media
        self.stdout.write(f'Copying media files from {media_root} to {static_media_dir}')
        
        # Walk through all directories in media_root
        for root, dirs, files in os.walk(media_root):
            # Get the relative path from media_root
            rel_path = os.path.relpath(root, media_root)
            if rel_path == '.':
                rel_path = ''
                
            # Create the corresponding directory in static_media_dir
            target_dir = os.path.join(static_media_dir, rel_path)
            os.makedirs(target_dir, exist_ok=True)
            
            # Copy all files
            for file in files:
                src_file = os.path.join(root, file)
                dst_file = os.path.join(target_dir, file)
                shutil.copy2(src_file, dst_file)
                self.stdout.write(f'Copied {src_file} to {dst_file}')
        
        self.stdout.write(self.style.SUCCESS('Successfully copied all media files to static directory'))
