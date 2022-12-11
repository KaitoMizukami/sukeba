from django.urls import path

from . import views


app_name = 'authentications'
urlpatterns = [ 
    path('login/', views.AuthenticationsLogin.as_view(), name='login'),
]