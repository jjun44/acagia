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
from acagiaApp.models import Event
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
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

@login_required
def events_by_date(request):
    """
    Shows events by a specific date.
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
