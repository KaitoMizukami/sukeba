from django.urls import path

from . import views


app_name = 'authentications'
urlpatterns = [ 
    path('signup/', views.AuthenticationsSignup.as_view(), name='signup'),
]