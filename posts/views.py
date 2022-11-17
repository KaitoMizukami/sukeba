from django.shortcuts import render
from django.views.generic import ListView

from .models import Post
from .prefectures import PREFECTURE_CHOICES


class PostsListView(ListView):
    """
    全ての投稿データを取得し,対応したHTMLに渡す
    """
    template_name = 'posts/posts_list.html'
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['prefectures'] = PREFECTURE_CHOICES
        return context


