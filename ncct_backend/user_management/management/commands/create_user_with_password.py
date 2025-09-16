from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.utils.crypto import get_random_string
from django.core.mail import send_mail

class Command(BaseCommand):
    help = 'Creates a new user, generates a random password, and sends it to the user\'s email.'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='The username for the new user')
        parser.add_argument('email', type=str, help='The email address for the new user')
        parser.add_argument('role', type=str, help='The role for the new user (Author, Curator, or Publisher)')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        role_name = options['role']

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.ERROR(f'User with username "{username}" already exists.'))
            return

        if role_name not in ['Author', 'Curator', 'Publisher']:
            self.stdout.write(self.style.ERROR(f'Invalid role "{role_name}". Must be one of Author, Curator, or Publisher.'))
            return

        password = get_random_string(12)
        user = User.objects.create_user(username=username, email=email, password=password)

        group = Group.objects.get(name=role_name)
        user.groups.add(group)

        send_mail(
            'Welcome to NCCT',
            f'Your account has been created. Your password is: {password}',
            'no-reply@ncct.com',
            [user.email],
            fail_silently=False,
        )

        self.stdout.write(self.style.SUCCESS(f'Successfully created user "{username}" and sent them an email with their password.'))
