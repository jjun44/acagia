from django.urls import path
from .views import SignUpCreateView, LogInCreateView

urlpatterns = [
    path('signup/', SignUpCreateView.as_view(), name='signup'),
    path('login/', LogInCreateView.as_view(), name='login')
]
