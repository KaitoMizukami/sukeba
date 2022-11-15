from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Location(models.Model):
    """
    スケートパークの情報に関するモデル
    """
    PREFECTURE_CHOICES = [ 
        ('北海道', '北海道'), ('青森県', '青森県'), ('岩手県', '岩手県'), ('宮城県', '宮城県'), ('秋田県', '秋田県'),
        ('山形県', '山形県'), ('福島県', '福島県'), ('茨城県', '茨城県'), ('栃木県', '栃木県'), ('群馬県', '群馬県'),
        ('埼玉県', '埼玉県'), ('千葉県', '千葉県'), ('東京都', '東京都'), ('神奈川県', '神奈川県'), ('新潟県', '新潟県'),
        ('富山県', '富山県'), ('石川県', '石川県'), ('福井県', '福井県'), ('山梨県', '山梨県'), ('長野県', '長野県'),
        ('岐阜県', '岐阜県'), ('静岡県', '静岡県'), ('愛知県', '愛知県'), ('三重県', '三重県'), ('滋賀県', '滋賀県'),
        ('京都府', '京都府'), ('大阪府', '大阪府'), ('兵庫県', '兵庫県'), ('奈良県', '奈良県'), ('和歌山県', '和歌山県'),
        ('鳥取県', '鳥取県'), ('島根県', '島根県'), ('岡山県', '岡山県'), ('広島県', '広島県'), ('山口県', '山口県'),
        ('徳島県', '徳島県'), ('香川県', '香川県'), ('愛媛県', '愛媛県'), ('高知県', '高知県'), ('福岡県', '福岡県'),
        ('佐賀県', '佐賀県'), ('長崎県', '長崎県'), ('熊本県', '熊本県'), ('大分県', '大分県'), ('宮崎県', '宮崎県'),
        ('鹿児島県', '鹿児島県'), ('沖縄県', '沖縄県'),
    ]
    name = models.CharField(max_length=50, verbose_name='パーク名')
    prefecture = models.CharField(max_length=4, choices=PREFECTURE_CHOICES, verbose_name='県名')
    city = models.CharField(max_length=10, verbose_name='市名')
    location_image = models.ImageField(upload_to='images/', verbose_name='写真')

    class Meta:
        verbose_name = 'スケートパーク'
        verbose_name_plural = 'スケートパーク'

    def __str__(self):
        return f'{self.name}({self.prefecture})'


class Post(models.Model):
    """ 
    投稿に関するモデル
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='投稿者')
    location = models.OneToOneField(Location, on_delete=models.CASCADE, verbose_name='スケートパーク')
    body = models.CharField(max_length=300, verbose_name='内容')
    # オブジェクトが最初に作成されたときに、フィールドを now に自動的に設定
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '投稿'
        verbose_name_plural = '投稿'

    def __str__(self):
        return self.body[:50]