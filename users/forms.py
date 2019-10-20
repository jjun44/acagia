from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, \
    AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder':'Username',
                                      'class':'form-control form-control-lg'})
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder':'Email Address',
                                      'class':'form-control form-control-lg'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder':'Password',
                                          'class':'form-control form-control-lg'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password',
                                          'class':'form-control form-control-lg'})
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)

class CustomUserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder':'Username',
                                      'class':'form-control form-control-lg'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder':'Password',
                                          'class':'form-control form-control-lg'})
    )

