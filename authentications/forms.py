from django import forms
from django.contrib.auth import get_user_model


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label='パスワード', min_length=8, widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='確認用パスワード', widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password')
    
    
