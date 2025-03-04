# backend/ncct_backend/user_management/management/commands/create_superuser.py
import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from dotenv import load_dotenv

class Command(BaseCommand):
    help = 'Create a superuser with predefined credentials'

    def handle(self, *args, **kwargs):
        load_dotenv()

        username = os.getenv('SUPERUSER_USERNAME')
        email = os.getenv('SUPERUSER_EMAIL')
        password = os.getenv('SUPERUSER_PASSWORD')

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists'))