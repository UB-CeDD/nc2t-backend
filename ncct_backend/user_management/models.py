from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.utils.crypto import get_random_string
from datetime import timedelta

# Profile model for storing additional user info like auth_code, auth_code_expiry
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    department = models.CharField(max_length=255, blank=True, null=True)
    auth_code = models.CharField(max_length=6, blank=True, null=True)
    auth_code_expiry = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def generate_auth_code(self):
        """Generates a random authentication code and sets expiration (1 hour)"""
        self.auth_code = get_random_string(6, allowed_chars='1234567890')
        self.auth_code_expiry = timezone.now() + timedelta(hours=1)
        self.save()

    def send_auth_code_email(self):
        """Sends an email with the authentication code to the user"""
        from django.core.mail import send_mail
        send_mail(
            'Complete Your Profile',
            f'Your authentication code is {self.auth_code}. It is valid for 1 hour.',
            'no-reply@example.com',
            [self.user.email],
            fail_silently=False,
        )

    def validate_auth_code(self, code):
        """Validates the authentication code and checks expiration"""
        if self.auth_code == code and timezone.now() <= self.auth_code_expiry:
            return True
        return False


# Role model with normalized permissions
class Role(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to Django User
    system_admin = models.CharField(max_length=255)
    fieldname = models.CharField(max_length=255)
    permissions = models.ManyToManyField(Permission)

    def __str__(self):
        return self.system_admin


# SpeciesRoleManager for assigning roles and permissions to users
class SpeciesRoleManager:
    def __init__(self, user):
        self.user = user

    def assign_role(self, role_name):
        """
        Assigns a role (group) to the user instance.
        Role names can be: Admin, Publisher, Curator, Author
        """
        group, created = Group.objects.get_or_create(name=role_name)
        self.user.groups.add(group)

    @classmethod
    def setup_roles(cls):
        """
        Set up roles and their permissions for the system.
        This method can remain class-based since it doesn't rely on an instance.
        """
        # Get the content type for the Species model
        species_content_type = ContentType.objects.get_for_model(Species)

        # Admin Group (Full permissions)
        admin_group, created = Group.objects.get_or_create(name='Admin')
        if created:
            admin_permissions = Permission.objects.filter(content_type=species_content_type)
            admin_group.permissions.set(admin_permissions)  # Admin has all permissions

        # Publisher Group (Full management of species)
        publisher_group, created = Group.objects.get_or_create(name='Publisher')
        if created:
            permissions = Permission.objects.filter(content_type=species_content_type, codename__in=['add_species', 'change_species', 'delete_species', 'view_species'])
            publisher_group.permissions.set(permissions)  # Full control over species

        # Curator Group (Review, but cannot publish or add species)
        curator_group, created = Group.objects.get_or_create(name='Curator')
        if created:
            permissions = Permission.objects.filter(content_type=species_content_type, codename__in=['view_species'])
            curator_group.permissions.set(permissions)  # Can only view species

        # Author Group (Manage species data but can't review or publish)
        author_group, created = Group.objects.get_or_create(name='Author')
        if created:
            permissions = Permission.objects.filter(content_type=species_content_type, codename__in=['add_species', 'change_species'])
            author_group.permissions.set(permissions)  # Can add and change species