from django.urls import path
from .views import *

urlpatterns = [
    path('', AcademyListView.as_view(), name='aca_list'),
    path('add_academy/', add_academy, name='add_academy'),
    path('dashboard/<int:pk>/', dashboard, name='dashboard'),
    path('members/<int:pk>/', member_list, name='mem_list'),
    path('members/add_member/<int:pk>/', add_member, name='add_member'),
    path('courses/<int:pk>/', CourseListView.as_view(), name='course_list'),
    path('courses/add_course/<int:pk>/', add_course,
         name='add_course'),
    path('checkin/<int:pk>/', check_in, name='check_in'),
    path('checkin/success/<int:pk>/', check_in_success,
         name='checkin_success')
]
