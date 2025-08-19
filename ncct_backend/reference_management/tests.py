from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Reference

class ReferenceSearchViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        self.reference1 = Reference.objects.create(
            type="journal",
            title="Test Journal 1",
            author="Author 1",
            doi="10.1000/test1"
        )
        self.reference2 = Reference.objects.create(
            type="thesis",
            title="Test Thesis 1",
            author="Author 2",
            thesis_level="PhD",
            doi="10.1000/test2"
        )

    def test_search_found_in_database(self):
        """
        Test that a search for a reference that exists in the database returns the correct data.
        """
        url = reverse('reference-search')
        response = self.client.get(url, {'q': 'journal'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.reference1.title)

    def test_search_not_found_in_database(self):
        """
        Test that a search for a reference that does not exist in the database returns the mocked web search results.
        """
        url = reverse('reference-search')
        response = self.client.get(url, {'q': 'biology'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('results', response.data)
        self.assertEqual(response.data['message'], "No results found in the database. Showing web search results.")

    def test_search_no_query_parameter(self):
        """
        Test that a search without a query parameter returns a 400 bad request.
        """
        url = reverse('reference-search')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
