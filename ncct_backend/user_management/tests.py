# backend/ncct_backend/user_management/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

class UserManagementTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.superuser = User.objects.create_superuser('admin', 'admin@nc2t.com', 'adminpassword')
        self.client.force_authenticate(user=self.superuser)
        self.user = User.objects.create_user('testuser', 'testuser@nc2t.com', 'testpassword')

    def test_list_users(self):
        response = self.client.get(reverse('user-list-create'))
        if response.status_code == status.HTTP_200_OK:
            print("\033[92mtest_list_users: PASSED\033[0m")
        else:
            print("\033[91mtest_list_users: FAILED\033[0m")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Expected status: 200 OK

    def test_create_user(self):
        data = {'username': 'newuser', 'email': 'newuser@nc2t.com', 'password': 'newpassword', 'role': 'Author'}
        response = self.client.post(reverse('admin-create-user'), data)
        if response.status_code == status.HTTP_201_CREATED:
            print("\033[92mtest_create_user: PASSED\033[0m")
        else:
            print("\033[91mtest_create_user: FAILED\033[0m")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Expected status: 201 Created

    def test_retrieve_user(self):
        response = self.client.get(reverse('user-detail', kwargs={'pk': self.user.pk}))
        if response.status_code == status.HTTP_200_OK:
            print("\033[92mtest_retrieve_user: PASSED\033[0m")
        else:
            print("\033[91mtest_retrieve_user: FAILED\033[0m")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Expected status: 200 OK

    def test_update_user(self):
        data = {'first_name': 'Updated'}
        response = self.client.patch(reverse('user-detail', kwargs={'pk': self.user.pk}), data)
        if response.status_code == status.HTTP_200_OK:
            print("\033[92mtest_update_user: PASSED\033[0m")
        else:
            print("\033[91mtest_update_user: FAILED\033[0m")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        # Expected status: 200 OK

    def test_soft_delete_user(self):
        data = {'is_active': False}
        response = self.client.patch(reverse('user-soft-delete', kwargs={'pk': self.user.pk}), data)
        if response.status_code == status.HTTP_200_OK:
            print("\033[92mtest_soft_delete_user: PASSED\033[0m")
        else:
            print("\033[91mtest_soft_delete_user: FAILED\033[0m")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)
        # Expected status: 200 OK

    def test_hard_delete_user(self):
        response = self.client.delete(reverse('user-hard-delete', kwargs={'pk': self.user.pk}))
        if response.status_code == status.HTTP_204_NO_CONTENT:
            print("\033[92mtest_hard_delete_user: PASSED\033[0m")
        else:
            print("\033[91mtest_hard_delete_user: FAILED\033[0m")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())
        # Expected status: 204 No Content