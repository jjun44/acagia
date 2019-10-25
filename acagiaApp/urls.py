from django.urls import path
from .views import *

urlpatterns = [
    path('', AcademyListView.as_view(), name='aca_list'),
    path('add_academy/', AcademyCreateView.as_view(), name='add_academy')
]
