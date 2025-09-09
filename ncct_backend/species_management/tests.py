from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Species, SpeciesUser
from ncct_backend.location_management.models import Location

User = get_user_model()

class SpeciesAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.location = Location.objects.create(name='Test Location')

    def test_create_species_assigns_author(self):
        """
        Ensure that when a species is created, the logged-in user is automatically assigned as the author.
        """
        url = '/api/v1/species/'
        data = {
            'name': 'Test Species',
            'family': 'Test Family',
            'harvest_sites': [self.location.id]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify that the species was created
        species = Species.objects.get(name='Test Species')
        self.assertIsNotNone(species)

        # Verify that the user was assigned as the author
        is_author = SpeciesUser.objects.filter(species=species, user=self.user, role='AUTHOR').exists()
        self.assertTrue(is_author)