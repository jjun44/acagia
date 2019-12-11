# ----------------------------------------------------------------------
# Name:        academy
# Purpose:     Handles requests for managing academies
#
# Date:        10/21/2019
# ----------------------------------------------------------------------
"""
Handles requests for managing academies and dashboard.
"""

from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe # for calender
from django.views.generic import CreateView, ListView, UpdateView
from acagiaApp.forms import AcademyForm
from acagiaApp.models import Academy, Member, Attendance, Event
from acagiaApp.utils import Calendar
from django.utils import timezone
from datetime import date, timedelta
import calendar
import pytz

DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%H:%M:%S'
DATETIME_FORMAT = '%a, %d %b %Y %I:%M %p'

@method_decorator(login_required, name='dispatch')
class AcademyListView(ListView):
    """
    Shows the list of academies owned by the user.
    """
    model = Academy
    template_name = 'acagiaApp/academy_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['academy_list'] = Academy.objects.filter(
            user_id=self.request.user.id
        )
        return context
'''
@login_required
def add_academy(request):
    """
    Add new academy information and its address information
    to the database.
    :param request: HTTP request
    :return: academy list page if academy is added successfully,
             otherwise, form page to prompt the user academy information
    """
    aca_form = AcademyForm()
    addr_form = AddressForm()
    if request.method == 'POST':
        aca_form = AcademyForm(request.POST)
        addr_form = AddressForm(request.POST)
        if aca_form.is_valid() and addr_form.is_valid():
            address = addr_form.save()
            academy = aca_form.save(commit=False)
            academy.user_id = request.user.id # Save user id as a f.k.
            academy.addr_id = address.id # Save address id as a f.k.
            academy.save()
            return redirect('/academy')

    return render(request, 'acagiaApp/academy_form.html', {
        'aca_form': aca_form
    })
'''
@method_decorator(login_required, name='dispatch')
class AcademyCreateView(CreateView):
    """
    Adds a new academy.
    """
    model = Academy
    form_class = AcademyForm
    template_name = 'acagiaApp/academy_form.html'
    success_url = reverse_lazy('aca_list')

    # https://www.agiliq.com/blog/2019/01/django-createview/
    # https://docs.djangoproject.com/en/2.2/topics/class-based-views/generic-editing/
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user_id = self.request.user.id
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['template'] = {'action_name': 'Add new academy to manage now!',
                               'btn_name': 'Add Academy'}
        return context

@method_decorator(login_required, name='dispatch')
class AcademyUpdateView(UpdateView):
    """
    Updates Academy information.
    """
    model = Academy
    form_class = AcademyForm
    template_name = 'acagiaApp/academy_form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        set_timezone(self.request, self.object)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['template'] = {'action_name': 'Update Academy Information',
                               'btn_name': 'Update'}
        return context

@login_required
def academy_info(request):
    """
    Shows academy information page
    """
    aca_id = request.session['aca_id']
    academy = Academy.objects.get(id=aca_id)
    template_name = 'acagiaApp/academy_info.html'
    return render(request, template_name, {'academy': academy})

# Set the current time zone
# https://docs.djangoproject.com/en/2.2/topics/i18n/timezones/
# https://stackoverflow.com/questions/27517259/django-activate-not-showing-effect
def set_timezone(request, academy):
    """
    Sets the user's timezone.
    :param request: HTTP request
    :param academy: current academy object
    """
    if academy.time_zone:
        request.session['django_timezone'] = academy.time_zone
        timezone.activate(pytz.timezone(academy.time_zone))
    else:
        timezone.deactivate()

@login_required
def dashboard(request, **kwargs):
    """
    Display a chosen user's academy dashboard with
    the academy information on the page including # of students
    and # of students attended today.
    :param request: HTTP request
    :param kwargs: keyword arguments including academy id
    :return: dashboard page with academy information
    """
    # Entered dashboard page initially?
    if kwargs.get('pk'):
        aca_id = kwargs['pk']
        request.session['aca_id'] = aca_id
        # Get the selected academy object
        academy = Academy.objects.get(id=aca_id)
        set_timezone(request, academy)
    # Revisitied from other tabs in the current dashboard?
    else:
        aca_id = request.session['aca_id']
        academy = Academy.objects.get(id=aca_id)

    today = timezone.localdate()
    members = Member.objects.filter(aca_id=aca_id)
    num_of_members = members.count()
    num_of_active = members.filter(status=Member.ACTIVE).count()
    num_of_inactive = members.filter(status=Member.INACTIVE).count()
    num_of_hold = members.filter(status=Member.HOLD).count()

    # Number of attended students today
    num_of_attended = Attendance.objects.filter(
        aca_id=aca_id, date_attended=today).count()
    # Birthday members
    bday_members = members.filter(
        date_of_birth__month=today.month,
        date_of_birth__day=today.day
    )
    # Birthday in next x days
    # https://stackoverflow.com/questions/6128921/queryset-of-people-with-a
    # -birthday-in-the-next-x-days
    #end_date = today + timedelta(days=7)

    return render(request, 'acagiaApp/dashboard.html',
                  {'academy': academy, 'num_mem':
                      num_of_members, 'num_active': num_of_active,
                   'num_inactive': num_of_inactive,
                   'num_hold': num_of_hold,
                   'num_att': num_of_attended,
                   'bday_members': bday_members,
                   'today': timezone.localtime().strftime(DATETIME_FORMAT)
                   })

@method_decorator(login_required, name='dispatch')
class CalendarView(ListView):
    """
    Shows a calendar view with prev/next links.
    """
    model = Event
    template_name = 'acagiaApp/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Use today's date for the calender view
        d = get_date(self.request.GET.get('month', None))

        # Instantiate the calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns the calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def get_date(req_day):
    """
    Gets a requested date to properly display monthly view.
    :param req_day: requested day from previous/next month
    :return: date to set a monthly view in the calendar.
    """
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        print('req_day: ', req_day)
        return date(year, month, day=1)
    print('here')
    return timezone.localdate()

def prev_month(d):
    """
    Sets a previous month for display.
    :param d: current day given
    :return: previous month
    """
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    print('prev_month: ', month)
    return month

def next_month(d):
    """
    Sets a next month for display.
    :param d: current day given
    :return: next month
    """
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    print('next_month: ', month)
    return month

@login_required
def settings(request):
    """
    Renders a setting page where users can manage academy settings
    """
    return render(request, 'acagiaApp/settings.html')
