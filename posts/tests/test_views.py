from django.test import TestCase, Client, RequestFactory
from django.urls import reverse

from posts.models import Location, Post
from posts.views import PostsListView
from posts.prefectures import PREFECTURE_CHOICES
from authentications.models import User


class PostsListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        location1 = Location(name='test1', prefecture='神奈川県', city='横浜市', location_image='test1')
        location1.save()
        location2 = Location(name='test1', prefecture='東京都', city='渋谷', location_image='test2')
        location2.save()
        post1 = Post(body='This is test1', location=location1)
        post1.author = User.objects.create(username='test1', email='test1@mail.com', password='testpassword')
        post1.save()
        post2 = Post(body='This is test2', location=location2)
        post2.author = User.objects.create(username='test2', email='test2@mail.com', password='testpassword')
        post2.save()

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create(username='loginuser', email='loginuser@mail.com', password='testpassword')
        self.url_name = 'posts:list'
        self.template_name = 'posts/posts_list.html'

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse(self.url_name))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse(self.url_name))
        self.assertTemplateUsed(response, self.template_name)

    def test_get_queryset_without_prefecture_query(self):
        request = self.factory.get(reverse(self.url_name))
        view = PostsListView()
        view.request = request
        qs = view.get_queryset()
        self.assertQuerysetEqual(qs, Post.objects.all(), ordered=False)

    def test_get_queryset_with_prefecture_query(self):
        """
        リクエストパラメーターありと無しでデータの数を比較し数が違ければテスト成功
        """
        request1 = self.factory.get(reverse(self.url_name), {'query': '神奈川県'})
        view1 = PostsListView()
        view1.request = request1
        qs1_count = view1.get_queryset().count
        request2 = self.factory.get(reverse(self.url_name))
        view2 = PostsListView()
        view2.request = request2
        qs2_count = view2.get_queryset().count
        self.assertNotEqual(qs1_count, qs2_count)

    def test_get_context_data(self):
        request = self.factory.get(reverse(self.url_name))
        response = PostsListView.as_view()(request)
        self.assertIsInstance(response.context_data, dict)
        self.assertEqual(response.context_data['prefectures'], PREFECTURE_CHOICES)


class PostsCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='testuser', email='test@mail.com')
        user.set_password('testpassword')
        user.save()

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.get(id=1)
        self.credentials = {
            'email': 'test@mail.com', 'password': 'testpassword'
        }
        self.url_name = 'posts:create'
        self.template_name = 'posts/posts_create.html'

    def test_view_url_exists_at_desired_location(self):
        _ = self.client.post(reverse('authentications:login'), self.credentials, follow=True)
        response = self.client.get('/posts/create/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        _ = self.client.post(reverse('authentications:login'), self.credentials, follow=True)
        response = self.client.get(reverse(self.url_name))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        _ = self.client.post(reverse('authentications:login'), self.credentials, follow=True)
        response = self.client.get(reverse(self.url_name))
        self.assertTemplateUsed(response, self.template_name)

    def test_view_redirect_to_login_page_if_not_authenticated(self):
        response = self.client.get(reverse(self.url_name), follow=True)
        self.assertTemplateUsed(response, 'authentications/authentications_login.html')

    