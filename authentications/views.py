from django.shortcuts import render, redirect
from django.views.generic import FormView, View, DetailView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth import get_user_model

from .forms import UserCreationForm, UserLoginForm


User = get_user_model()


class UnauthenticatedOnly(UserPassesTestMixin):
    """
    ログイン済みのユーザーのアクセスを制限する
    """
    def test_func(self):
        # ログイン状態じゃないかチェック
        return not self.request.user.is_authenticated
    
    def handle_no_permission(self):
        # ログイン状態なら投稿一覧へリダイレクト
        return redirect('posts:list')


class AuthenticationsSignupView(UnauthenticatedOnly, FormView):
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


class AuthenticationsLoginView(UnauthenticatedOnly, FormView):
    template_name = 'authentications/authentications_login.html'
    form_class = UserLoginForm

    def post(self, request, *args, **kwargs):
        """ 
        Postリクエスト時の処理
        送信されたメールアドレスとパスワードでユーザーを検索し見つかったらログインする
        見つからなかったらログインページを返す
        """
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('posts:list')
        return redirect('authentications:login')
        

class AuthenticationsLogoutView(View):
    """
    ログアウト機能　HTMLファイルはなし
    """
    def get(self, request):
        logout(request)
        return redirect('authentications:login')


class UserProfileView(DetailView):
    """
    特定のユーザーの投稿一覧を取得しHTMLを返す
    """
    model = User
    template_name = 'authentications/user_profile.html'

    def get(self, request, pk):
        user = User.objects.get(id=pk)
        user_posts = user.post_set.all()
        context = {
            'user': user,
            'posts': user_posts
        }
        return render(request, 'authentications/user_profile.html', context)