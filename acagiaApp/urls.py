from django.urls import path
from .views import *

urlpatterns = [
    path('', AcademyListView.as_view(), name='aca_list'),
    path('add-academy/', AcademyCreateView.as_view(), name='add_academy'),
    path('update-academy/<int:pk>/', AcademyUpdateView.as_view(),
         name='update_aca'),

    # Entered dashboard initially
    path('dashboard/<int:pk>/', dashboard, name='first_dashboard'),
    # Home tab clicked in the current dashboard
    path('dashboard/', dashboard, name='dashboard'),

    path('members/', member_list, name='mem_list'),
    path('members/add-member/', MemberCreateView.as_view(), name='add_member'),
    path('members/delete-member/<int:pk>/',
         MemberDeleteView.as_view(),
         name='delete_member'),
    path('members/update-member/<int:pk>/', MemberUpdateView.as_view(),
         name='update_member'),
    path('members/detail/<int:pk>/', member_detail_view, name='mem_detail'),

    path('courses/', CourseListView.as_view(), name='course_list'),
    path('courses/add-course/', add_course,
         name='add_course'),
    path('courses/delete-course/<int:pk>/', CourseDeleteView.as_view(),
         name='delete_course'),
    path('courses/update-course/<int:pk>/', CourseUpdateView.as_view(),
         name='update_course'),

    path('checkin/', check_in, name='check_in'),
    path('checkin/success/', check_in_success,
         name='checkin_success'),

    path('attendance/', AttendanceListView.as_view(), name='att_list'),
    path('attendance/delete-record/<int:pk>/', AttendanceDeleteView.as_view(),
         name='delete_att'),
    path('attendance/update-record/<int:pk>/', AttendanceUpdateView.as_view(),
         name='update_att'),
    path('attendance/add-record/', AttendanceCreateView.as_view(),
         name='add_att'),

    path('rank-sys/', RankSystemListView.as_view(), name='rank_sys_list'),
    path('rank-sys/add-rank/', add_rank, name='add_rank'),
    path('rank-sys/delete-rank/<int:pk>/', RankDeleteView.as_view(),
         name='delete_rank'),
    path('rank-sys/update-rank/<int:pk>/', RankUpdateView.as_view(),
         name='update_rank'),
]
