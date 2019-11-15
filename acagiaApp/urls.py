from django.urls import path
from .views import *

urlpatterns = [
    # ACADEMY
    path('', AcademyListView.as_view(), name='aca_list'),
    path('add-academy/', AcademyCreateView.as_view(), name='add_academy'),
    path('update-academy/<int:pk>/', AcademyUpdateView.as_view(),
         name='update_aca'),

    # DASHBOARD
    # Entered dashboard initially
    path('dashboard/<int:pk>/', dashboard, name='first_dashboard'),
    # Home tab clicked in the current dashboard
    path('dashboard/', dashboard, name='dashboard'),
    path(r'dashboard/^calendar/$', CalendarView.as_view(), name='cal'),

    # MEMBERS
    path('members/', member_list, name='mem_list'),
    path('members/add-member/', MemberCreateView.as_view(), name='add_member'),
    path('members/delete-member/<int:pk>/',
         MemberDeleteView.as_view(),
         name='delete_member'),
    path('members/update-member/<int:pk>/', MemberUpdateView.as_view(),
         name='update_member'),
    path('members/detail/<int:pk>/', member_detail_view, name='mem_detail'),

    # PROMOTION
    path('promotion/', promotion_list, name='promo_list'),
    path('promotion/update-rank/<int:pk>/', MemberRankUpdateView.as_view(),
         name='update_mem_rank'),

    # COURSES
    path('courses/', CourseListView.as_view(), name='course_list'),
    path('courses/add-course/', add_course,
         name='add_course'),
    path('courses/delete-course/<int:pk>/', CourseDeleteView.as_view(),
         name='delete_course'),
    path('courses/update-course/<int:pk>/', CourseUpdateView.as_view(),
         name='update_course'),

    # EVENTS
    path('events/', EventListView.as_view(), name='event_list'),
    path('events/add-event/', EventCreateView.as_view(), name='add_event'),

    # CHECK-IN
    path('checkin/', check_in, name='check_in'),
    path('checkin/success/', check_in_success,
         name='checkin_success'),

    # ATTENDANCE
    path('attendance/', attendance_by_date, name='att_by_date'),

    # RANKING SYSTEM
    path('rank-sys/', RankSystemListView.as_view(), name='rank_sys_list'),
    path('rank-sys/add-rank/', add_rank, name='add_rank'),
    path('rank-sys/delete-rank/<int:pk>/', RankDeleteView.as_view(),
         name='delete_rank'),
    path('rank-sys/update-rank/<int:pk>/', RankUpdateView.as_view(),
         name='update_rank'),

    # SETTINGS
    path('settings/', settings, name='settings'),
    # Manage academy info
    path('settings/aca_info/', academy_info, name='aca_info'),
    # Manage attendance records
    path('settings/att/', AttendanceListView.as_view(), name='att_list'),
    path('settings/att/delete-record/<int:pk>/',
         AttendanceDeleteView.as_view(),
         name='delete_att'),
    path('settings/att/update-record/<int:pk>/',
         AttendanceUpdateView.as_view(),
         name='update_att'),
    path('settings/att/add-record/', AttendanceCreateView.as_view(),
         name='add_att'),

]
