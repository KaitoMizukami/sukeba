from django.test import TestCase

from authentications.models import User


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='testuser', email='test@mail.com')
        user.set_password('testpassword')
        user.save()
    
    def setUp(self):
        self.user = User.objects.get(id=1)

    def test_email_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('email').verbose_name
        self.assertEqual(field_label, 'メールアドレス')
    
    def test_username_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('username').verbose_name
        self.assertEqual(field_label, 'ユーザーネーム')
    
    def test_email_max_length_250(self):
        user = User.objects.get(id=1)
        max_length = user._meta.get_field('email').max_length
        self.assertEqual(max_length, 250)

    def test_email_unique(self):
        user = User.objects.get(id=1)
        is_unique = user._meta.get_field('email').unique
        self.assertTrue(is_unique)
    
    def test_username_max_length_100(self):
        user = User.objects.get(id=1)
        max_length = user._meta.get_field('username').max_length
        self.assertTrue(max_length, 100)

    def test_user_is_not_staff_by_default(self):
        self.assertFalse(self.user.is_staff)

    def test_user_is_not_superuser_by_default(self):
        self.assertFalse(self.user.is_superuser)

    def test_set_is_active_by_default(self):
        self.assertTrue(self.user.is_active)

    def test_user_object_as_string_is_equal_to_username(self):
        self.assertEqual(str(self.user), self.user.username)
    
    def test_can_create_a_user(self):
        before_count = User.objects.all().count
        _ = User.objects.create_user(
            email='test1@mail.com', username='test', password='testpassword'
        )
        after_count = User.objects.all().count
        self.assertNotEqual(before_count, after_count)

    def test_raise_error_if_email_is_empty(self):
        with self.assertRaises(ValueError):
            _ = User.objects.create_user(email='', username='test', password='testpassword')

    def test_raise_error_if_username_is_empty(self):
        with self.assertRaises(ValueError):
            _ = User.objects.create_user(email='test@mail.com', username='', password='testpassword')

    def test_email_should_normalize(self):
        email = 'test2@MAIL.COM'
        user = User.objects.create_user(
            email='test2@mail.com', username='test', password='testpassword'
        )
        self.assertEqual(user.email, email.lower())

    def test_password_should_be_hashed(self):
        password = 'testpassword'
        user = User.objects.create_user(
            email='test3@mail.com', username='test', password=password
        )
        self.assertNotEqual(password, user.password)

    def test_can_create_a_speruser(self):
        superuser = User.objects.create_superuser(
            email='test4@mail.com', username='test', password='testpassword'
        )
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)