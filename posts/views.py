from django.shortcuts import render, redirect
from django.views.generic import (
    ListView, CreateView, DetailView
)
from django.db.models import Q

from .models import Post
from .prefectures import PREFECTURE_CHOICES
from .forms import PostForm, LocationForm


class PostsListView(ListView):
    """
    全ての投稿データを取得し,対応したHTMLに渡す
    """
    template_name = 'posts/posts_list.html'
    model = Post

    def get_queryset(self, **kwargs):
        """ 
        デフォルトでPostモデルの全てのデータをリストで返す
        queryキーワードがある場合はマッチしたPostモデルのデータをリストで返す
        """
        queryset = super().get_queryset(**kwargs)
        # GETリクエストパラメータにqueryがあれば、それでフィルタする
        query_keyword = self.request.GET.get('query')
        if query_keyword:
            # locationモデルのprefectureとquery_keywordが一致するデータをフィルタする
            queryset = Post.objects.filter(
                Q(location__prefecture__contains=query_keyword)
            )
        return queryset

    def get_context_data(self, **kwargs):
        """
        テンプレートに渡すコンテキストにデータを加える
        """
        context = super().get_context_data(**kwargs)
        # 全都道府県のリストをコンテキストに追加
        context['prefectures'] = PREFECTURE_CHOICES
        return context


class PostsCreateView(CreateView):
    """ 
    投稿の作成フォームをHTMLに渡す
    Postメソッドでリクエストが来たらフォームの検証をし保存する
    """
    template_name = 'posts/posts_create.html'

    def get(self, request):
        """ 
        Getリクエスト時の処理
        PostとLocationモデルのフォーム2つをHTMLに渡す
        """
        post_form = PostForm()
        location_form = LocationForm()
        context = {
            'post_form': post_form,
            'location_form': location_form
        }
        return render(request, 'posts/posts_create.html', context)

    def post(self, request, *args, **kwargs):
        """ 
        Postリクエスト時の処理
        Post, Loationモデルのフォームを検証しデータを保存する
        検証成功すれば投稿一覧ページにリダイレクトし、失敗したら同じページを返す
        """
        post_form = PostForm(request.POST, prefix='post')
        location_form = LocationForm(request.POST, request.FILES, prefix='location')
        print(location_form)
        if post_form.is_valid() and location_form.is_valid():
            new_location = location_form.save()
            # postモデルのオブジェクトを作成
            # commit=Falseでまだデータベースには保存されない
            new_post = post_form.save(commit=False)
            new_post.location = new_location
            new_post.author = request.user
            new_post.save()
            return redirect('posts:list')
        context = {
            'post_form': post_form,
            'location_form': location_form
        }
        return render(request, 'posts/posts_create.html', context)


class PostsDetailView(DetailView):
    template_name = 'posts/posts_detail.html'
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['prefectures'] = PREFECTURE_CHOICES
        return context