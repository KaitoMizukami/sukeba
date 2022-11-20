from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

from .prefectures import PREFECTURE_CHOICES


User = get_user_model()


class Common(models.Model):
    """
    抽象モデル
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='投稿者')
    # オブジェクトが最初に作成されたときに、フィールドを now に自動的に設定
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='投稿日')

    class Meta:
        abstract = True


class Location(models.Model):
    """
    スケートパークの情報に関するモデル
    """
    name = models.CharField(max_length=50, verbose_name='パーク名')
    prefecture = models.CharField(max_length=4, choices=PREFECTURE_CHOICES, verbose_name='県名')
    city = models.CharField(max_length=10, verbose_name='市名')
    location_image = models.ImageField(upload_to='images/', verbose_name='写真')

    class Meta:
        verbose_name = 'スケートパーク'
        verbose_name_plural = 'スケートパーク'

    def __str__(self):
        return f'{self.name}({self.prefecture})'


class Post(Common):
    """ 
    投稿に関するモデル
    """
    location = models.OneToOneField(Location, on_delete=models.CASCADE, verbose_name='スケートパーク')
    body = models.CharField(max_length=300, verbose_name='内容')

    class Meta:
        verbose_name = '投稿'
        verbose_name_plural = '投稿'

    def __str__(self):
        return self.body[:50]

    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'pk': self.pk})


class Comment(Common):
    """ 
    投稿のコメントに関するモデル
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.CharField(max_length=150, verbose_name='コメント内容')

    class Meta:
        verbose_name = 'コメント'
        verbose_name_plural = 'コメント'
    
    def __str__(self):
        return self.body[:50]
    