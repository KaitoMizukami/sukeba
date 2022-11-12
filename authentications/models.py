from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)


class UserManager(BaseUserManager):
    """
    ユーザーを作成する関数。戻り値は作ったユーザーオブジェクト 
    """
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('メールアドレスは必須です')
        if not username:
            raise ValueError('ユーザーネームは必須です')
        
        email = self.normalize_email(email) # ドメイン部分を小文字にして、メールアドレスを正規化
        user = self.model(
            username=username,
            email=email,  
        )
        user.set_password(password) # ハッシュ化されたパスワードを作成
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        """
        スーパーユーザーを作成する関数。戻り値は作ったユーザーオブジェクト 
        """
        super_user = self.create_user(email, username, password)
        super_user.is_staff = True
        super_user.is_superuser = True
        super_user.save(using=self._db)
        return super_user


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

    objects = UserManager()

    USERNAME_FIELD = 'email' # Userモデルを一意に識別するフィールド
    REQUIRED_FIELDS = ['username'] # createsuperuserコマンドでユーザー作成する時の追加フィールド

    def __str__(self):
        return self.username