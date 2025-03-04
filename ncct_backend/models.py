# from django.db import models
# from django.contrib.auth.models import Group, Permission, User
# from django.contrib.contenttypes.models import ContentType
#
# # Species model
# class Species(models.Model):
#     unique_id = models.AutoField(primary_key=True)
#     compound_code = models.IntegerField()
#     ref = models.ForeignKey('Reference', on_delete=models.CASCADE)
#     collection_data = models.TextField()
#
#     def __str__(self):
#         return f"Species {self.unique_id}"
#
# class SpeciesRoleManager:
#     def __init__(self, user):
#         self.user = user
#
#     def assign_role(self, role_name):
#         """
#         Assigns a role (group) to the user instance.
#         Role names can be: Admin, Publisher, Curator, Author
#         """
#         group, created = Group.objects.get_or_create(name=role_name)
#         self.user.groups.add(group)
#
#     @classmethod
#     def setup_roles(cls):
#         """
#         Set up roles and their permissions for the system.
#         This method can remain class-based since it doesn't rely on an instance.
#         """
#         # Get the content type for the Species model
#         species_content_type = ContentType.objects.get_for_model(Species)
#
#         # Admin Group (Full permissions)
#         admin_group, created = Group.objects.get_or_create(name='Admin')
#         if created:
#             admin_permissions = Permission.objects.filter(content_type=species_content_type)
#             admin_group.permissions.set(admin_permissions)  # Admin has all permissions
#
#         # Publisher Group (Full management of species)
#         publisher_group, created = Group.objects.get_or_create(name='Publisher')
#         if created:
#             permissions = Permission.objects.filter(content_type=species_content_type, codename__in=['add_species', 'change_species', 'delete_species', 'view_species'])
#             publisher_group.permissions.set(permissions)  # Full control over species
#
#         # Curator Group (Review, but cannot publish or add species)
#         curator_group, created = Group.objects.get_or_create(name='Curator')
#         if created:
#             permissions = Permission.objects.filter(content_type=species_content_type, codename__in=['view_species'])
#             curator_group.permissions.set(permissions)  # Can only view species
#
#         # Author Group (Manage species data but can't review or publish)
#         author_group, created = Group.objects.get_or_create(name='Author')
#         if created:
#             permissions = Permission.objects.filter(content_type=species_content_type, codename__in=['add_species', 'change_species'])
#             author_group.permissions.set(permissions)  # Can add and change species
#
# # Compound model
# class Compound(models.Model):
#     subclass = models.CharField(max_length=255, primary_key=True)
#     compound_class = models.CharField(max_length=255)
#     smiles = models.TextField()
#
#     def __str__(self):
#         return f"Compound {self.subclass}"
#
# # Species-Compound many-to-many relationship
# class SpeciesCompound(models.Model):
#     species = models.ForeignKey(Species, on_delete=models.CASCADE)
#     compound = models.ForeignKey(Compound, on_delete=models.CASCADE)
#
#     class Meta:
#         unique_together = (('species', 'compound'),)  # Ensure that the same combination is unique
#
#     def __str__(self):
#         return f"{self.species.unique_id} - {self.compound.subclass}"
#
# # Location model
# class Location(models.Model):
#     unique_id = models.AutoField(primary_key=True)
#     continent = models.CharField(max_length=255)
#     country = models.CharField(max_length=255)
#     region_state = models.CharField(max_length=255)
#     city_town = models.CharField(max_length=255)
#     place = models.CharField(max_length=255)
#     gps_latitude = models.DecimalField(max_digits=9, decimal_places=6)
#     gps_longitude = models.DecimalField(max_digits=9, decimal_places=6)
#
#     def __str__(self):
#         return f"{self.city_town}, {self.country}"
#
# # Site model
# class Site(models.Model):
#     unique_id = models.AutoField(primary_key=True)
#     location = models.ForeignKey(Location, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return f"Site {self.unique_id}"
#
# # Species-Site many-to-many relationship
# class SpeciesSite(models.Model):
#     species = models.ForeignKey(Species, on_delete=models.CASCADE)
#     site = models.ForeignKey(Site, on_delete=models.CASCADE)
#
#     class Meta:
#         unique_together = (('species', 'site'),)
#
#     def __str__(self):
#         return f"{self.species.unique_id} - {self.site.unique_id}"
#
# # Herbarium model
# class Herbarium(models.Model):
#     unique_id = models.AutoField(primary_key=True)
#     location = models.ForeignKey(Location, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return f"Herbarium {self.unique_id}"
#
# # Species-Herbarium many-to-many relationship
# class SpeciesHerbarium(models.Model):
#     species = models.ForeignKey(Species, on_delete=models.CASCADE)
#     herbarium = models.ForeignKey(Herbarium, on_delete=models.CASCADE)
#
#     class Meta:
#         unique_together = (('species', 'herbarium'),)
#
#     def __str__(self):
#         return f"{self.species.unique_id} - {self.herbarium.unique_id}"
#
# # Address model (normalized from JSON)
# class Address(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='address')  # Link to Django User
#     street = models.CharField(max_length=255)
#     city = models.CharField(max_length=255)
#     country = models.CharField(max_length=255)
#
#     def __str__(self):
#         return f"{self.street}, {self.city}, {self.country}"
#
# # Reference model
# class Reference(models.Model):
#     unique_id = models.AutoField(primary_key=True)
#     type = models.CharField(max_length=255)
#     title = models.CharField(max_length=255)
#     author = models.CharField(max_length=255)
#     thesis_level = models.CharField(max_length=255, blank=True, null=True)
#
#     def __str__(self):
#         return self.title
#
# # Permissions model
# class Permission(models.Model):
#     unique_id = models.AutoField(primary_key=True)
#     permission = models.CharField(max_length=255)
#
#     def __str__(self):
#         return self.permission
#
# # Role model with normalized permissions
# class Role(models.Model):
#     id = models.AutoField(primary_key=True, default=1)  # Default value for existing rows
#     user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to Django User
#     system_admin = models.CharField(max_length=255)
#     fieldname = models.CharField(max_length=255)
#     permissions = models.ManyToManyField(Permission)
#
#     def __str__(self):
#         return self.system_admin