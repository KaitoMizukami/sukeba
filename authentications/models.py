from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        max_length=250, unique=True,
        verbose_name='メールアドレス'
    )
    username = models.CharField(max_length=100, verbose_name='ユーザーネーム')
    instagram_username = models.CharField(
        max_length=100, blank=True, null=True,
        verbose_name='インスタグラムのユーザーネーム',
        help_text='任意です'
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email' # Userモデルを一意に識別するフィールド
    REQUIRED_FIELDS = ['username'] # createsuperuserコマンドでユーザー作成する時の追加フィールド

    def __str__(self):
        return self.username