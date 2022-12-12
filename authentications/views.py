from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.contrib.auth import authenticate, login

from .forms import UserCreationForm, UserLoginForm


class AuthenticationsSignup(FormView):
    template_name = 'authentications/authentications_signup.html'
    form_class = UserCreationForm

    def post(self, request, *args, **kwargs):
        """ 
        Postリクエスト時の処理
        Userモデルのフォームを検証し、データを保存する
        検証成功すれば投稿一覧ページにリダイレクトし、自動でログインした状態にする
        検証失敗すれば登録ページを返す
        """
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            user = authenticate(email=user_form.cleaned_data['email'], password=user_form.cleaned_data['password'])
            login(request, user)
            return redirect('posts:list')
        else:
            return redirect('authentications:signup')


class AuthenticationsLoginView(FormView):
    template_name = 'authentications/authentications_login.html'
    form_class = UserLoginForm

    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email, password)
        if user is not None:
            login(request, user)
            return redirect('posts:list')
        return redirect('authentications:login')
        