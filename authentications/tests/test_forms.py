from django.test import TestCase

from authentications.forms import UserCreationForm
from authentications.models import User


class UserCreationFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            'password': 'testpassword',
            'confirm_password': 'testpassword',
            'email': 'test@mail.com',
            'username': 'test'
        }
        form = UserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_if_password_is_empty(self):
        form_data = {
            'password': '',
            'confirm_password': 'testpassword',
            'email': 'test@mail.com',
            'username': 'test'
        }
        form = UserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_form_if_confirm_password_is_empty(self):
        form_data = {
            'password': 'testpassword',
            'confirm_password': '',
            'email': 'test@mail.com',
            'username': 'test'
        }
        form = UserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_invalid_form_if_email_is_empty(self):
        form_data = {
            'password': 'testpassword',
            'confirm_password': 'testpassword',
            'email': '',
            'username': 'test'
        }
        form = UserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_form_if_username_is_empty(self):
        form_data = {
            'password': 'testpassword',
            'confirm_password': 'testpassword',
            'email': 'test@mail.com',
            'username': ''
        }
        form = UserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_if_two_password_is_not_same(self):
        form_data = {
            'password': 'testpassword',
            'confirm_password': 'aaaaaaaaa',
            'email': 'test@mail.com',
            'username': 'test'
        }
        form = UserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_can_create_a_new_user(self):
        before_count = User.objects.all().count
        form_data = {
            'password': 'testpassword',
            'confirm_password': 'testpassword',
            'email': 'test1@mail.com',
            'username': 'test'
        }
        form = UserCreationForm(form_data)
        form.save()
        after_count = User.objects.all().count
        self.assertNotEqual(before_count, after_count)