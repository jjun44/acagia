from django.urls import path
from .views import SignUpCreateView, LogInCreateView, LoginErrorView

urlpatterns = [
    path('signup/', SignUpCreateView.as_view(), name='signup'),
    path('login/', LogInCreateView.as_view(), name='login'),
    path('login-error', LoginErrorView.as_view(), name='login_error')
]
