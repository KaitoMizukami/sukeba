from django.contrib import admin

from .models import Post, Location


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # 投稿モデルの表示に使用されるフィールド
    list_display = ('author', 'location', 'body',)
    fieldsets = (
        ('投稿', {
            'fields': (
                'author', 'location', 'body',
            )
        }),
    )
     # 1つのフィールドでユーザーを絞り込む
    list_filter = ('author',)

    # 検索される時に使われるフィールド
    search_fields = ('author', 'location',)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'prefecture', 'city')
    fieldsets = (
        ('スケートパーク', {
            'fields': (
                'name', 
                'prefecture',
                'city',
                'location_image',
            )
        }),
    )
    # 2つのフィールドでユーザーを絞り込む
    list_filter = ('prefecture', 'city',)

    # 検索される時に使われるフィールド
    search_fields = ('name',)