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
        self.signup_template = 'authentications/authentications_signup.html'
        self.credentials = {
            'email': 'test@mail.com', 'password': 'testpassword'
        }
        self.url_name = 'authentications:signup'

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse(self.url_name))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse(self.url_name))
        self.assertTemplateUsed(response, self.signup_template)

    def test_view_creates_a_new_user(self):
        before_count = User.objects.all().count
        response = self.client.post(reverse(self.url_name), {
            'username': 'testuser', 'email': 'test@mail.com',
            'password': 'testpassword', 'confirm_password': 'testpassword'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        after_count = User.objects.all().count
        self.assertNotEqual(before_count, after_count)
    
    def test_authenticated_user_redirect_to_main_page(self):
        _ = self.client.post(reverse('authentications:login'), self.credentials)
        response = self.client.get(reverse(self.url_name))
        # リダイレクト(302)が発生したかテスト
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse(self.url_name), follow=True)
        # リダイレクト先のHTMLファイルを確認
        self.assertTemplateNotUsed(response, self.signup_template)
        self.assertTemplateUsed(response, 'posts/posts_list.html')

    def test_view_render_signup_page_if_form_is_invalid(self):
        response = self.client.post(reverse(self.url_name), {})
        self.assertTemplateUsed(response, self.signup_template)


class AuthenticationsLoginViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='testuser', email='test@mail.com')
        user.set_password('testpassword')
        user.save()

    def setUp(self):
        self.client = Client()
        self.login_template = 'authentications/authentications_login.html'
        self.credentials = {
            'email': 'test@mail.com', 'password': 'testpassword'
        }
        self.url_name = 'authentications:login'

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse(self.url_name))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse(self.url_name))
        self.assertTemplateUsed(response, self.login_template)

    def test_view_can_login(self):
        response = self.client.post(reverse(self.url_name), self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_authenticated_user_redirect_to_main_page(self):
        response = self.client.post(reverse(self.url_name), self.credentials, follow=True)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse(self.url_name), follow=True)
        self.assertTemplateUsed(response, 'posts/posts_list.html')

    def test_redirect_to_login_page_if_user_not_found(self):
        response = self.client.post(reverse(self.url_name), {
            'email': 'aaaaa@mail.com', 'password': 'aaaaaaaaa'
        }, follow=True)
        self.assertTemplateUsed(response, self.login_template)