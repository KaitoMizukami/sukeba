from django.shortcuts import render
from django.views.generic import FormView

from .forms import UserCreationForm


class AuthenticationsSignup(FormView):
    template_name = 'authentications/authentications_signup.html'
    form_class = UserCreationForm

    
