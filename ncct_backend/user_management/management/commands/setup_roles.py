from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from ncct_backend.species_management.models import Species

class Command(BaseCommand):
    help = 'Sets up default user roles and permissions'

    def handle(self, *args, **options):
        self.stdout.write('Setting up default user roles...')

        # Get content types for relevant models
        try:
            species_content_type = ContentType.objects.get_for_model(Species)
            user_content_type = ContentType.objects.get_for_model(User)
            group_content_type = ContentType.objects.get_for_model(Group)
        except ContentType.DoesNotExist:
            self.stderr.write(self.style.ERROR('One or more models not found. Ensure all relevant apps are migrated.'))
            return

        # Define roles and their permissions
        roles_permissions = {
            'Admin': [
                # User permissions
                ('add_user', user_content_type),
                ('change_user', user_content_type),
                ('delete_user', user_content_type),
                ('view_user', user_content_type),
                # Group permissions
                ('add_group', group_content_type),
                ('change_group', group_content_type),
                ('delete_group', group_content_type),
                ('view_group', group_content_type),
                # Species permissions (all)
                ('add_species', species_content_type),
                ('change_species', species_content_type),
                ('delete_species', species_content_type),
                ('view_species', species_content_type),
            ],
            'Author': [
                ('add_species', species_content_type),
                ('change_species', species_content_type),
                ('view_species', species_content_type),
            ],
            'Curator': [
                ('view_species', species_content_type),
                ('change_species', species_content_type),
            ],
            'Publisher': [
                ('add_species', species_content_type),
                ('change_species', species_content_type),
                ('delete_species', species_content_type),
                ('view_species', species_content_type),
            ],
        }

        for role_name, permissions_list in roles_permissions.items():
            group, created = Group.objects.get_or_create(name=role_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created group: {role_name}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Group {role_name} already exists.'))

            # Clear existing permissions for the group to ensure a clean slate
            group.permissions.clear()

            for codename, content_type in permissions_list:
                try:
                    permission = Permission.objects.get(content_type=content_type, codename=codename)
                    group.permissions.add(permission)
                    self.stdout.write(self.style.SUCCESS(f'  Added permission {codename} to {role_name}'))
                except Permission.DoesNotExist:
                    self.stderr.write(self.style.WARNING(f'  Permission {codename} for {content_type.model} not found. Skipping.'))

        self.stdout.write(self.style.SUCCESS('Default user roles setup complete.'))
