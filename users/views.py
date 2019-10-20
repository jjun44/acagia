from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm, CustomUserLoginForm


class SignUpCreateView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class LogInCreateView(LoginView):
    form_class = CustomUserLoginForm
    success_url = reverse_lazy('home')
    template_name = 'registration/login.html'