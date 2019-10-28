from django.urls import path
from .views import *

urlpatterns = [
    path('', AcademyListView.as_view(), name='aca_list'),
    path('add_academy/', add_academy, name='add_academy'),
    path('dashboard/<int:pk>/', dashboard, name='dashboard'),
    path('students/<int:pk>/', student_list, name='stu_list'),
    path('students/add_student/<int:pk>', add_student, name='add_student')
]
