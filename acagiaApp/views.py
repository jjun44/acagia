from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .forms import AcademyForm, MemberForm, CourseForm, CheckInForm, \
    MemberUpdateForm, AttendanceForm, RankFormset, RankForm, MemberRankForm
from .models import Academy, Member, Attendance, Course, Rank, MemberRank
from django.contrib import messages
from django.utils import timezone
from datetime import date, timedelta
from django.db import IntegrityError
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
        context['template'] = {'action_name': 'Add New Academy',
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

@login_required
def member_list(request):
    """
    Shows the list of members in the academy with basic information.
    :param request: HTTP request
    :param kwargs: keyword arguments including academy id
    :return: member list page
    """
    # Get current academy's members
    aca_id = request.session['aca_id']
    member_list = Member.objects.filter(
        aca_id=aca_id
    ).order_by('first_name')
    return render(request, 'acagiaApp/member_list.html',
                  {'members': member_list})

@method_decorator(login_required, name='dispatch')
class MemberCreateView(CreateView):
    """
    Adds a new member.
    """
    model = Member
    form_class = MemberForm
    template_name = 'acagiaApp/member_form.html'
    success_url = reverse_lazy('mem_list')

    # https://www.agiliq.com/blog/2019/01/django-createview/
    # https://docs.djangoproject.com/en/2.2/topics/class-based-views/generic-editing/
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.aca_id = self.request.session['aca_id']
        self.object.member_since = timezone.localdate()
        self.object.save()
        # Create member's rank with default value
        member_rank = MemberRank(member_id=self.object.id,
                                 aca_id=self.object.aca_id)
        member_rank.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['template'] = {'action_name': 'Add New Member', 'btn_name':
            'Add Member'}
        return context

@method_decorator(login_required, name='dispatch')
class MemberDeleteView(DeleteView):
    """
    Deletes a selected member and redirects to a member list page.
    """
    model = Member

    def get_success_url(self):
        # How to pass kwargs?
        # https://stackoverflow.com/questions/46915320/reverse-got-an-unexpected-keyword-argument-pk-url-kwarg-updateview
        return reverse('mem_list')

@method_decorator(login_required, name='dispatch')
class MemberUpdateView(UpdateView):
    """
    Updates existing member information.
    """
    model = Member
    form_class = MemberUpdateForm
    success_url = reverse_lazy('mem_list')
    template_name = 'acagiaApp/member_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['template'] = {'action_name': 'Update Member', 'btn_name':
            'Update'}
        return context

@login_required
def member_detail_view(request, **kwargs):
    """
    Displays selected member's detailed information.
    :param request: HTTP request
    :param kwargs: keyword arguments including member id
    :return:
    """
    member = Member.find_member_by_id(mem_id=kwargs['pk'])
    return render(request, 'acagiaApp/member_detail.html', {'member': member})

@method_decorator(login_required, name='dispatch')
class CourseListView(ListView):
    """
    Shows the list of courses in the academy.
    """
    model = Course
    template_name = 'acagiaApp/course_list.html'

    def get_context_data(self, **kwargs):
        aca_id = self.request.session['aca_id']
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.filter(
            aca_id=aca_id
        )
        return context

'''
@method_decorator(login_required, name='dispatch')
class CourseCreateView(CreateView):
    model = Course
    form_class = CourseForm
    success_url = reverse_lazy('course_list')
    template_name = 'acagiaApp/course_form.html'

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        
        form = self.form_class(aca_id=pk)
        return render(request, self.template_name, {'form': form, 'aca_id':pk})

    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        form = self.form_class(request.POST, aca_id=pk)
        if form.is_valid():
            form.save()
            return render(request, 'acagiaApp/course_list.html',
                          {'aca_id': pk})
        return render(request, self.template_name,
                      {'form': form, 'aca_id': pk})
'''

@login_required
def add_course(request, **kwargs):
    """
    Adds a new course to Course table.
    :param request: HTTP request
    :param kwargs: keyword arguments including academy id
    :return: course list page if course is added successfully,
             otherwise, form page to prompt the course information
    """
    # Pass aca_id to the form.
    # https://stackoverflow.com/questions/28653699/passing-request-object-from-view-to-form-in-django
    aca_id = request.session['aca_id']
    form = CourseForm(aca_id=aca_id)
    template = {'action_name': 'Add New Class', 'btn_name':
        'Add Class'}
    if request.method == 'POST':
        form = CourseForm(request.POST, aca_id=aca_id)
        if form.is_valid():
            course = form.save(commit=False)
            course.aca_id = aca_id
            # Save instructor's id
            if form.cleaned_data['instructor']:
                course.instructor_id = form.cleaned_data['instructor'].id
            form.save()
            return redirect('/academy/courses/')
    return render(request, 'acagiaApp/course_form.html',
                      {'form': form, 'template': template})

@method_decorator(login_required, name='dispatch')
class CourseDeleteView(DeleteView):
    """
    Deletes a selected course and redirects to a course list page.
    """
    model = Course

    def get_success_url(self):
        return reverse('course_list')

@method_decorator(login_required, name='dispatch')
class CourseUpdateView(UpdateView):
    """
    Updates an existing course.
    """
    model = Course
    form_class = CourseForm
    success_url = reverse_lazy('course_list')
    template_name = 'acagiaApp/course_form.html'

    # Pass aca_id to the form.
    # https://stackoverflow.com/questions/28653699/passing-request-object-from-view-to-form-in-django
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'aca_id': self.request.session['aca_id']})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['template'] = {'action_name': 'Update Class', 'btn_name':
            'Update'}
        return context

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
            increase_days(member.id)
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

def increase_days(id):
    """
    Increases member's days attended at the current rank.
    :param id: (Number) member id
    """
    # Get the given member's rank object
    mem_rank = MemberRank.objects.get(member_id=id)
    mem_rank.days_attended += 1
    mem_rank.total_days += 1
    mem_rank.save()

def reset_days(member):
    """
    Resets member's days attended at the current rank to 0
    when he/she gets promoted or demoted (whenever rank changes).
    :param member: (MemberRank) given member's rank object
    """
    member.days_attended = 0

@method_decorator(login_required, name='dispatch')
class AttendanceListView(ListView):
    """
    Shows the list of attendance records.
    """
    model = Attendance
    template_name = 'acagiaApp/att_list.html'

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

@login_required
def add_rank(request):
    aca_id = request.session['aca_id']
    if request.method == 'GET':
        formset = RankFormset(request.GET or None)
    elif request.method == 'POST':
        formset = RankFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                try:
                    rank = form.save(commit=False)
                    rank.aca_id = aca_id
                    form.save()
                except IntegrityError:
                    redirect('/academy/rank-sys/add-rank/')

            return redirect('/academy/rank-sys/')
        else:
            msg = 'Please complete all fields correctly. ' \
                  'Make sure to enter whole numbers for rank order ' \
                  '(e.g. 1) and days required (e.g. 30). '
            messages.error(request, msg)

    return render(request, 'acagiaApp/rank_multi_forms.html', {
        'formset': formset,
        'action_name': 'Add New Rank',
        'btn_name': 'Add Rank'
    })

@method_decorator(login_required, name='dispatch')
class RankDeleteView(DeleteView):
    """
    Deletes selected rank information and redirects to the rank system page.
    """
    model = Rank

    def get_success_url(self):
        return reverse('rank_sys_list')

@method_decorator(login_required, name='dispatch')
class RankUpdateView(UpdateView):
    """
    Updates existing member information.
    """
    model = Rank
    form_class = RankForm
    success_url = reverse_lazy('rank_sys_list')
    template_name = 'acagiaApp/rank_single_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['template'] = {'action_name': 'Update Rank', 'btn_name':
            'Update'}
        return context

'''
@method_decorator(login_required, name='dispatch')
class RankSystemListView(ListView):
    """
    Shows the list of Ranking systems customized by the user.
    """
    model = Rank
    template_name = 'acagiaApp/rank_system_list.html'

    def get_context_data(self, **kwargs):
        aca_id = self.request.session['aca_id']
        context = super().get_context_data(**kwargs)
        # Get all the rank info associated with the academy
        ranks = Rank.objects.filter(aca_id=aca_id)
        # Get the list of rank types used in the academy
        # flat option will return only the values not including column names
        rank_types = list(ranks.values_list('rank_type', flat=True).distinct())
        rank_systems = {}
        for type in rank_types:
            # Get all ranks associated with each rank type in the rank order
            # defer excludes columns specified
            rank_systems[type] = list(ranks.filter(rank_type=type).order_by(
                'rank_order').defer('id', 'aca_id'))
        context['rank_systems'] = rank_systems
        return context
'''

@method_decorator(login_required, name='dispatch')
class RankSystemListView(ListView):
    """
    Shows the list of Ranking system customized by the user.
    """
    model = Rank
    template_name = 'acagiaApp/rank_system_list.html'

    def get_context_data(self, **kwargs):
        aca_id = self.request.session['aca_id']
        context = super().get_context_data(**kwargs)
        # Get all the ranks associated with the academy in ascending order
        # Defer excludes columns specified
        ranks = Rank.objects.filter(aca_id=aca_id).order_by(
            'rank_order').defer('id', 'aca_id')
        context['ranks'] = ranks
        context['academy'] = Academy.objects.get(
            id=aca_id)
        return context

@login_required
def promotion_list(request):
    aca_id = request.session['aca_id']
    template_name = 'acagiaApp/promotion_list.html'
    # Get all members in alphabetical order
    members = MemberRank.objects.filter(aca_id=aca_id).order_by(
        'member__first_name')
    # Get all ranks in order
    all_ranks = Rank.objects.filter(aca_id=aca_id).order_by('rank_order')
    # If no rank system is made, sends an error message.
    if not all_ranks:
        messages.info(request, 'Make your ranking system first to use '
                               'PROMOTION tab now!')
        return redirect('/academy/rank-sys/')
    first_rank = all_ranks.first() # Get the first rank in the ranking system
    last_rank = all_ranks.last() # Get the last rank in the ranking system
    promotion_list = [] # All members' promotion info
    # Go through each member and set pre/current/next rank and days left
    for member in members:
        mem_rank = {} # Each member's promotion info will be saved
        if not member.rank: # Member isn't assigned a rank yet
            pre = 'X'
            current = 'X'
            next = first_rank
        else: # Member is currently associated with a rank
            current = member.rank # Get the current rank
            '''
            If member isn't at his first rank, previous rank will be the 
            rank in the order that is the last smaller rank than the current 
            rank's order.
            If member isn't at his last rank, next rank will be the rank
            in the order that is the smallest larger rank than the current 
            rank's order. 
            '''
            # when there's only 1 rank
            if current == first_rank and current == last_rank:
                pre = 'X'
                next = 'X'
            elif current == first_rank: # Member is at first rank
                pre = 'X'
                next = all_ranks.filter(
                    rank_order__gt=member.rank.rank_order).first()
            elif current == last_rank: # Member is at last rank
                pre = all_ranks.filter(
                    rank_order__lt=member.rank.rank_order).last()
                next = 'X'
            else:
                pre = all_ranks.filter(
                    rank_order__lt=member.rank.rank_order).last()
                next = all_ranks.filter(
                    rank_order__gt=member.rank.rank_order).first()

        if current == 'X' or next == 'X':
            days_left = 'X'
        else:
            days_left = current.days_required - member.days_attended
        # if current is set to X, calculate days left with 0
        mem_rank = {'id': member.id, 'name': member.member, 'pre': pre,
                    'current': current, 'next': next, 'days_left': days_left
                    }
        promotion_list.append(mem_rank) # Append to list of all members

    # When promote button clicked
    if request.method == 'POST' and 'promote_btn' in request.POST:
        promote_demote(request, 'promote', members, all_ranks)
        return redirect('/academy/promotion/')

    # When demote button clicked
    if request.method == 'POST' and 'demote_btn' in request.POST:
        promote_demote(request, 'demote', members, all_ranks)
        return redirect('/academy/promotion/')

    return render(request, template_name, {'prom_list': promotion_list})

def promote_demote(request, operation, members, ranks):
    """
    Handles promotion and demotion of selected members.
    :param request: HTTP request
    :param operation: (string) indicates either promote or demote
    :param members: (MemberRank) members in the academy
    :param ranks: (Rank) all ranks used in the academy
    """
    # Messages to send to the user
    error_msg = 'You didn\'t select any members! Please select members first.'
    fail_msg = ' members are failed to be ' + operation + 'd: '
    success_msg = ' members ' + operation + 'd successfully: '
    # Get all selected member ids
    selected_ids = request.POST.getlist('members')
    # number of failed members
    num_fail = 0
    num_success = 0

    # No members selected? send error msg and return.
    if not selected_ids:
        messages.error(request, error_msg)
        return

    # For each id, find the member and promote.
    for id in selected_ids:
        member = members.get(id=id)
        next = None
        pre = None
        # Get pre or next rank
        if not member.rank:  # Member isn't assigned a rank yet
            if operation == 'promote':
                next = ranks.first() # next rank will be the first rank
        else:
            if operation == 'demote':
                pre = ranks.filter(rank_order__lt=member.rank.rank_order).last()
            else:
                next = ranks.filter(rank_order__gt=member.rank.rank_order).first()
        # No more higher rank to promote?
        if operation == 'promote' and not next:
            # Set error msg indicating who's failed and decrease # of success
            fail_msg += str(member.member) + ', '
            num_fail += 1
        # No more lower rank to demote?
        elif operation == 'demote' and not pre:
            fail_msg += str(member.member) + ', '
            num_fail += 1
        else:
            success_msg += str(member.member) + ', '
            if operation == 'promote':
                member.rank = next
            else:
                member.rank = pre
            num_success += 1
            reset_days(member)
            member.save()

    # Send successful message if 1 or more members are promoted
    if num_success > 0:
        messages.success(request, str(num_success) + success_msg[0:-2])
    # Send fail message if 1 or more members are failed to be promoted
    if num_fail > 0:
        messages.error(request, str(num_fail) + fail_msg[0:-2])

@method_decorator(login_required, name='dispatch')
class MemberRankUpdateView(UpdateView):
    """
    Updates member's ranking information.
    """
    model = MemberRank
    form_class = MemberRankForm
    success_url = reverse_lazy('promo_list')
    template_name = 'acagiaApp/member_rank_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'aca_id': self.request.session['aca_id']})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['template'] = {'action_name': 'Update Rank', 'btn_name':
            'Update'}
        return context
    