# ----------------------------------------------------------------------
# Name:        events
# Purpose:     Handles requests for managing events
#
# Date:        11/11/2019
# ----------------------------------------------------------------------
"""
Handles requests for managing events.
"""

from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from acagiaApp.forms import EventForm, AttendanceDateForm
from acagiaApp.models import Event, Member
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from .attendance import increase_days
import pytz

@method_decorator(login_required, name='dispatch')
class EventCreateView(CreateView):
    """
    Adds a new event.
    """
    model = Event
    form_class = EventForm
    success_url = reverse_lazy('event_list')
    template_name = 'acagiaApp/event_form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.aca_id = self.request.session['aca_id']
        #self.object.start_time = localize_datetime(self.request,
        # self.object.start_time)
        #self.object.end_time = localize_datetime(self.request,
        #                                          self.object.end_time)
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['template'] = {'action_name': 'Create New Event',
                               'btn_name': 'Create Event'}
        return context

def localize_datetime(request, dt):
    tz = pytz.timezone(request.session['django_timezone'])
    print(tz)
    print(dt)
    new_dt = tz.localize(dt.replace(tzinfo=None))
    print(new_dt)
    return new_dt

'''
@method_decorator(login_required, name='dispatch')
class EventListView(ListView):
    """
    Shows the list of events in the academy.
    """
    model = Event
    template_name = 'acagiaApp/event_list.html'

    def get_context_data(self, **kwargs):
        aca_id = self.request.session['aca_id']
        context = super().get_context_data(**kwargs)
        context['events'] = Event.objects.filter(
            aca_id=aca_id
        )
        return context
'''

@login_required
def events_by_date(request):
    """
    Shows events by a specific date.
    Default date is today when entering the Events tab initially
    or when there's no event found with the given date.
    """
    aca_id = request.session['aca_id']
    template_name = 'acagiaApp/event_list.html'
    form = AttendanceDateForm
    today = timezone.localdate() # Get today
    all_events = Event.objects.filter(aca_id=aca_id) # Get all events
    # Get today's events
    events = all_events.filter(Q(start_date__lte=today) &
                               Q(end_date__gte=today)).order_by('start_time')
    #events = all_events.filter(Q(start_time__contains=today) |
    #                         (Q(start_time__lte=today) & Q(
    #                         end_time__gte=today)))
    num = events.count()
    day = 'Today'
    # When specific date is given by the user, search records by the date
    if request.method == 'POST':
        form = AttendanceDateForm(request.POST)
        if form.is_valid():
            input_date = form.cleaned_data['date_attended']
            events = all_events.filter(Q(start_date__lte=input_date) &
                                       Q(end_date__gte=input_date)).order_by('start_time')
            num = events.count()
            day = 'on ' + str(input_date)
            if not events:
                msg = 'No events found on ' + str(input_date)
                messages.error(request, msg)
                return redirect('/academy/events/')

    return render(request, template_name, {'form': form, 'events': events,
                                           'num': num, 'day' : day})

@method_decorator(login_required, name='dispatch')
class EventUpdateView(UpdateView):
    """
    Updates event information.
    """
    model = Event
    form_class = EventForm
    template_name = 'acagiaApp/event_form.html'
    success_url = reverse_lazy('event_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['template'] = {'action_name': 'Update Event', 'btn_name':
            'Update'}
        return context

@method_decorator(login_required, name='dispatch')
class EventDeleteView(DeleteView):
    """
    Deletes a selected event.
    """
    model = Event

    def get_success_url(self):
        return reverse('event_list')

@login_required
def add_members_to_event(request, **kwargs):
    """
    Gives a given credit for attendance to all selected event attendees.
    :param kwargs: includes event id
    :return:
    """
    aca_id = request.session['aca_id']
    event_id = kwargs['pk']
    template_name = 'acagiaApp/event_add_members.html'
    # Get all members in alphabetical order
    members = Member.objects.filter(aca_id=aca_id).order_by('first_name')
    # Get clicked event
    event = Event.objects.get(id=event_id)

    if request.method == 'POST':
        error_msg = 'Please select members.'
        # Get all selected members
        selected_ids = request.POST.getlist('members')
        # Get the input credit entered by the user
        #credit = request.POST.get('credits')
        if give_credits(selected_ids, event.credit):
            reverse_lazy('event_list')
        else:
            messages.error(request, error_msg)

    return render(request, template_name, {'members': members, 'event': event})

def validate_number(num):
    """
    Checks if the given number is a positive integer number and not empty.
    :param num: number or string
    :return: true if num is valid, otherwise, false
    """
    if is_integer(num):
        num = int(num)
        if num < 0:
            return False
        return True
    else:
        return False

def is_integer(n):
    """
    Checks if n is an integer, not a string nor float number.
    :param n: given number or string to validate
    :return: True if n is integer, otherwise, false
    """
    try:
        int(n)
    except ValueError:
        return False
    else:
        if isinstance(n, float):
            return False
        else:
            return True

def give_credits(member_ids, credit):
    """

    :param request:
    :param members:
    :return: true if giving credit was done successfully, otherwise, false
    """
    # No members selected? send error msg and return
    print(member_ids, credit)
    if not member_ids or not validate_number(credit):
        return False
    # Give credit to each selected member
    for id in member_ids:
        increase_days(id, int(credit))
    return True