from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .forms import UserCreationForm, UserChangeForm


class CustomUserAdmin(UserAdmin):
    # ユーザーインスタンスを追加、変更するためのフォーム
    form = UserChangeForm
    add_form = UserCreationForm

    # ユーザーモデルの表示に使用されるフィールド
    list_display = ('email', 'username', 'is_staff')
    fieldsets = (
        ('ユーザー情報', {'fields': (
            'username', 'email', 'password', 'instagram_username'
        )}),
        ('パーミッション', {'fields': (
            'is_active', 'is_staff', 'is_superuser'
        )})
    )

    # ユーザーインスタンスを作成する時に必要なフィールド
    add_fieldsets = (
        ('ユーザユーザー情報', {'fields': (
            'username','email', 'password', 'confirm_password'
        )})
    )