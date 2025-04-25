import os
import mimetypes
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files.base import ContentFile
from cloudinary import uploader

from agent.models import Agent, Post
from agent.cloudinary_storage import CloudinaryMediaStorage

class Command(BaseCommand):
    help = 'Migrates existing media files to Cloudinary'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Perform a dry run without actually uploading files',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if not settings.USE_CLOUDINARY_STORAGE:
            self.stdout.write(self.style.WARNING('Cloudinary storage is not configured. Aborting.'))
            return
        
        self.stdout.write('Starting migration of media files to Cloudinary...')
        
        # Create a Cloudinary storage instance
        storage = CloudinaryMediaStorage()
        
        # Migrate agent profile pictures
        self._migrate_agent_images(storage, dry_run)
        
        # Migrate post images
        self._migrate_post_images(storage, dry_run)
        
        self.stdout.write(self.style.SUCCESS('Migration completed successfully!'))
    
    def _migrate_agent_images(self, storage, dry_run):
        """Migrate Agent profile pictures to Cloudinary."""
        self.stdout.write("Migrating Agent profile pictures...")
        
        agents = Agent.objects.all()
        for agent in agents:
            if agent.profile_picture and not agent.profile_picture.name.startswith('http'):
                try:
                    file_name = agent.profile_picture.name
                    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
                    
                    if os.path.exists(file_path):
                        self.stdout.write(f"  Migrating {file_name}...")
                        
                        if not dry_run:
                            # Read the file content
                            with open(file_path, 'rb') as f:
                                file_content = f.read()
                            
                            # Upload to Cloudinary
                            storage._save(file_name, ContentFile(file_content))
                            
                            self.stdout.write(self.style.SUCCESS(f"  Migrated {file_name}"))
                    else:
                        self.stdout.write(self.style.WARNING(f"  File not found: {file_path}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"  Error migrating {agent.profile_picture.name}: {e}"))
    
    def _migrate_post_images(self, storage, dry_run):
        """Migrate Post images to Cloudinary."""
        self.stdout.write("Migrating Post images...")
        
        posts = Post.objects.all()
        for post in posts:
            if post.image and not post.image.name.startswith('http'):
                try:
                    file_name = post.image.name
                    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
                    
                    if os.path.exists(file_path):
                        self.stdout.write(f"  Migrating {file_name}...")
                        
                        if not dry_run:
                            # Read the file content
                            with open(file_path, 'rb') as f:
                                file_content = f.read()
                            
                            # Upload to Cloudinary
                            storage._save(file_name, ContentFile(file_content))
                            
                            self.stdout.write(self.style.SUCCESS(f"  Migrated {file_name}"))
                    else:
                        self.stdout.write(self.style.WARNING(f"  File not found: {file_path}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"  Error migrating {post.image.name}: {e}"))
