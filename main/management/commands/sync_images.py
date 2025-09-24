# Create: main/management/commands/sync_images.py
from django.core.management.base import BaseCommand
import shutil
import os
from django.conf import settings

class Command(BaseCommand):
    def handle(self, *args, **options):
        media_path = os.path.join(settings.BASE_DIR, 'media', 'menu_images')
        static_path = os.path.join(settings.BASE_DIR, 'main', 'static', 'main', 'images')
        
        if os.path.exists(media_path):
            for filename in os.listdir(media_path):
                src = os.path.join(media_path, filename)
                dst = os.path.join(static_path, filename)
                shutil.copy2(src, dst)
                self.stdout.write(f"Copied {filename}")