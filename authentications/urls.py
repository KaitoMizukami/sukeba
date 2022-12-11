from django.urls import path

from . import views


app_name = 'authentications'
urlpatterns = [ 
    path('login/', views.AuthenticationsSignup.as_view(), name='signup'),
]