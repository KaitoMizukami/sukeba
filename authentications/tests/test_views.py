from django.test import TestCase, Client
from django.urls import reverse

from authentications.models import User


class AuthenticationsSignupViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='testuser', email='test@mail.com')
        user.set_password('testpassword')
        user.save()

    def setUp(self):
        self.client = Client()

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('authentications:signup'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('authentications:signup'))
        self.assertTemplateUsed(response, 'authentications/authentications_signup.html')

    def test_view_creates_a_new_user(self):
        before_count = User.objects.all().count
        response = self.client.post(reverse('authentications:signup'), {
            'username': 'testuser', 'email': 'test@mail.com',
            'password': 'testpassword', 'confirm_password': 'testpassword'
        }, follow=True)
        after_count = User.objects.all().count
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(before_count, after_count)
    
    def test_authenticated_user_redirect_to_main_page(self):
        _ = self.client.post(reverse('authentications:login'), {
            'email': 'test@mail.com', 'password': 'testpassword'
        })
        response = self.client.get(reverse('authentications:signup'))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('authentications:signup'), follow=True)
        self.assertTemplateNotUsed(response, 'authentications/authentications_signup.html')
        self.assertTemplateUsed(response, 'posts/posts_list.html')

    def test_view_render_signup_page_if_form_is_invalid(self):
        response = self.client.post(reverse('authentications:signup'), {})
        self.assertTemplateUsed(response, 'authentications/authentications_signup.html')