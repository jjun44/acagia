# ----------------------------------------------------------------------
# Name:        attendance
# Purpose:     Handles requests for attendance and check-in systems
#
# Date:        11/1/2019
# ----------------------------------------------------------------------
"""
Handles requests for attendance and check-in systems.
"""

from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from acagiaApp.forms import CheckInForm, AttendanceForm, AttendanceDateForm
from acagiaApp.models import Member, Attendance, MemberRank
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count

TIME_FORMAT = '%H:%M:%S'

@login_required
def check_in(request):
    """
    Checks in a student once he/she enters a correct name.
    :param request: HTTP request
    :return: successful page if checking-in is done successfully,
             otherwise, form page to prompt the student a name
    """
    aca_id = request.session['aca_id']
    form = CheckInForm(aca_id=aca_id)
    if request.method == 'POST':
        form = CheckInForm(request.POST, aca_id=aca_id)
        if form.is_valid():
            record = form.save(commit=False)
            record.aca_id = aca_id # Save academy id
            # Get entered name
            fname = form.cleaned_data['first_name']
            lname = form.cleaned_data['last_name']
            # If wrong name, show an error message
            member = Member.find_member_by_name(aca_id, fname, lname)
            if member is None:
                # How to use django messages
                # https://simpleisbetterthancomplex.com/tips/2016/09/06
                # /django-tip-14-messages-framework.html
                messages.error(request, 'Please check your name and enter '
                                        'again!')
                return render(request, 'acagiaApp/checkin_form.html',
                              {'form': form})
            record.member_id = member.id # Save matching member id
            # Save course id
            record.course_id = form.cleaned_data['course'].id
            record.date_attended = timezone.localdate()
            record.time_attended = timezone.localtime().strftime(TIME_FORMAT)
            form.save()
            increase_days(member.id, 1)
            return redirect('/academy/checkin/success/')
    return render(request, 'acagiaApp/checkin_form.html',
                  {'form': form})

@login_required
def check_in_success(request, **kwargs):
    """
    Displays a checked-in successful message.
    :param request:
    :param kwargs:
    :return:
    """
    return render(request, 'acagiaApp/checkin_success.html')

def increase_days(id, credit):
    """
    Increases member's days attended at the current rank by amount of credit.
    :param id: (Number) member id
    :param credit: (Number) credit for attendance
    """
    # Get the given member's rank object
    mem_rank = MemberRank.objects.get(member_id=id)
    mem_rank.days_attended += credit
    #mem_rank.days_left -= credit
    #mem_rank.total_days += credit
    mem_rank.save()

def decrease_days(id, credit):
    """
    Decreases member's days attended at the current rank by amount of credit.
    :param id: (Number) member id
    :param credit: (Number) credit for attendance
    """
    mem_rank = MemberRank.objects.get(member_id=id)
    mem_rank.days_attended -= credit
    #mem_rank.days_left += credit
    #mem_rank.total_days -= credit
    mem_rank.save()
'''
@login_required
def attendance_by_date(request):
    """
    Shows a specific date's attendance records.
    """
    aca_id = request.session['aca_id']
    template_name = 'acagiaApp/att_date_list.html'
    # When specific date is given by the user, search records by the date
    if request.method == 'POST':
        form = AttendanceDateForm(request.POST)
        if form.is_valid():
            input_date = form.cleaned_data['date_attended']
            records = Attendance.objects.filter(aca_id=aca_id,
                                                date_attended=input_date)
            num = records.count()
            day = 'on ' + str(input_date)
            group_attendance(records)
            if not records:
                msg = 'No records found on ' + str(input_date)
                messages.error(request, msg)
                return redirect('/academy/attendance/')
    else: # When date isn't given, set date as today by default
        form = AttendanceDateForm
        today = timezone.localdate()  # Get today
        # Get today's attendance records
        records = Attendance.objects.filter(aca_id=aca_id, date_attended=today)
        num = records.count()
        day = 'Today'
        group_attendance(records)

    return render(request, template_name, {'form': form, 'records': records,
                                           'num': num, 'day' : day})
'''
@login_required
def attendance_by_date(request):
    """
    Shows today's or specific date's attendance records.
    """
    aca_id = request.session['aca_id']
    template_name = 'acagiaApp/att_date_list.html'
    grouped_list = []
    # When specific date is given by the user, search records by the date
    if request.method == 'POST':
        form = AttendanceDateForm(request.POST)
        if form.is_valid():
            input_date = form.cleaned_data['date_attended']
            records = Attendance.objects.filter(aca_id=aca_id,
                                                date_attended=input_date)
            num = records.count()
            day = 'on ' + str(input_date)
            group_attendance(grouped_list, records)
            if not records:
                msg = 'No records found on ' + str(input_date)
                messages.error(request, msg)
                return redirect('/academy/attendance/')
    else: # When date isn't given, set date as today by default
        form = AttendanceDateForm
        today = timezone.localdate()  # Get today
        # Get today's attendance records
        records = Attendance.objects.filter(aca_id=aca_id, date_attended=today)
        num = records.count()
        day = 'Today'
        group_attendance(grouped_list, records)

    return render(request, template_name, {'form': form, 'records': grouped_list,
                                           'num': num, 'day' : day})

def group_attendance(grouped_list, records):
    """
    Group attendance records by course and sort by course start time.
    :param records: filtered attendance records by date
    :return: (dictionary) key:course, value:records
    """
    """
    # Group records by courses
    for record in records:
        grouped_records[record.course] = []

    # Add attendance records to the corresponding course
    for record in records:
        grouped_records[record.course].append(record.member)

    # Count records in each course
    for record in grouped_records:
        grouped_records[record].insert(0, len(grouped_records[record]))
    """
    grouped_records = {}
    for record in records:
        grouped_records[record.course] = []
    for record in records:
        grouped_records[record.course].append(record.member)

    # Separate each course with its attendees and add number of attendees
    for record in grouped_records:
        sub_dict = {}
        sub_dict['course'] = record
        sub_dict['attendees'] = grouped_records[record]
        sub_dict['count'] = len(grouped_records[record])
        grouped_list.append(sub_dict)

    print(grouped_list)

@method_decorator(login_required, name='dispatch')
class AttendanceListView(ListView):
    """
    Shows the list of attendance records.
    """
    model = Attendance
    template_name = 'acagiaApp/att_manage_list.html'

    def get_context_data(self, **kwargs):
        aca_id = self.request.session['aca_id']
        context = super().get_context_data(**kwargs)
        context['records'] = Attendance.objects.filter(
            aca_id=aca_id).order_by('-date_attended', '-time_attended')
        return context

@method_decorator(login_required, name='dispatch')
class AttendanceDeleteView(DeleteView):
    """
    Deletes a selected course and redirects to a course list page.
    """
    model = Attendance

    def get_success_url(self):
        return reverse('att_list')

@method_decorator(login_required, name='dispatch')
class AttendanceUpdateView(UpdateView):
    """
    Updates an existing attendance record.
    """
    model = Attendance
    form_class = AttendanceForm
    success_url = reverse_lazy('att_list')
    template_name = 'acagiaApp/attendance_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'aca_id': self.request.session['aca_id']})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['template'] = {'action_name': 'Update Attendance Record',
                               'btn_name':
            'Update'}
        return context

@method_decorator(login_required, name='dispatch')
class AttendanceCreateView(CreateView):
    """
    Adds a new attendance record.
    """
    model = Attendance
    form_class = AttendanceForm
    success_url = reverse_lazy('att_list')
    template_name = 'acagiaApp/attendance_form.html'

    def get_form_kwargs(self):
        # pass kwargs to form
        kwargs = super().get_form_kwargs()
        kwargs.update({'aca_id': self.request.session['aca_id']})
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.aca_id = self.request.session['aca_id']
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['template'] = {'action_name': 'Add New Attendance Record',
                               'btn_name': 'Add Record'}
        return context