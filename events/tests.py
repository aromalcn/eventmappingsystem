from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        # Create a user for login tests
        self.user = User.objects.create_user(
            username='existinguser', 
            email='existing@example.com', 
            password='testpassword123'
        )

    def test_register_view_status(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)

    def test_login_view_status(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)

    def test_registration_with_email(self):
        """Test that a user can register with an email address."""
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        })
        if response.status_code == 200:
            print(response.context['form'].errors)
        self.assertRedirects(response, reverse('map_home'))
        
        # Verify user is created
        User = get_user_model()
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())

    def test_login_with_username(self):
        """Test login with username."""
        response = self.client.post(self.login_url, {
            'username': 'existinguser',
            'password': 'testpassword123'
        })
        self.assertRedirects(response, reverse('map_home'))
        
        # Check if logged in
        response = self.client.get(reverse('map_home'))
        self.assertContains(response, 'Welcome, existinguser!')

    def test_login_with_email(self):
        """Test login with email address."""
        response = self.client.post(self.login_url, {
            'username': 'existing@example.com', # The form field is still 'username'
            'password': 'testpassword123'
        })
        self.assertRedirects(response, reverse('map_home'))
        
        # Check if logged in
        response = self.client.get(reverse('map_home'))
        self.assertContains(response, 'Welcome, existinguser!')

    def test_logout(self):
        self.client.login(username='existinguser', password='testpassword123')
        response = self.client.post(self.logout_url)
        self.assertRedirects(response, reverse('login'))
