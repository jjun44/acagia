from django.shortcuts import render, redirect, render_to_response
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from users.models import CustomUser as User
from .forms import AcademyForm, MemberForm, CourseForm, AttendanceForm
from .models import Academy, Member, Attendance, Course
from datetime import date
from django.contrib import messages

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
    # Revisitied from other tabs in the current dashboard?
    else:
        aca_id = request.session['aca_id']
    academy = Academy.objects.get(id=aca_id)
    num_of_students = Member.objects.filter(aca_id=aca_id).count()
    num_of_attended = Attendance.objects.filter(
        aca_id=aca_id, date_attended=date.today()).count()
    return render(request, 'acagiaApp/dashboard.html',
                  {'academy': academy, 'num_stu':
                      num_of_students,
                   'num_att': num_of_attended})

@login_required
def member_list(request, **kwargs):
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
    )
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
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['template'] = {'action_name': 'Add a New Member', 'btn_name':
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
    Updates an existing course.
    """
    model = Member
    form_class = MemberForm
    success_url = reverse_lazy('mem_list')
    template_name = 'acagiaApp/member_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['template'] = {'action_name': 'Update a Member', 'btn_name':
            'Update'}
        return context

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
    template = {'action_name': 'Add a Class', 'btn_name':
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
        context['template'] = {'action_name': 'Update a Class', 'btn_name':
            'Update'}
        return context

@login_required
def check_in(request, **kwargs):
    """
    Checks in a student once he/she enters a correct name.
    :param request: HTTP request
    :return: successful page if checking-in is done successfully,
             otherwise, form page to prompt the student a name
    """
    aca_id = request.session['aca_id']
    form = AttendanceForm(aca_id=aca_id)
    if request.method == 'POST':
        form = AttendanceForm(request.POST, aca_id=aca_id)
        if form.is_valid():
            record = form.save(commit=False)
            record.aca_id = aca_id # Save academy id
            # Get entered name
            fname = form.cleaned_data['first_name']
            lname = form.cleaned_data['last_name']
            # If wrong name, show an error message
            member = find_member(aca_id, fname, lname)
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
            form.save()
            return redirect('/academy/checkin/success/')
    return render(request, 'acagiaApp/checkin_form.html',
                      {'form': form})

def find_member(aca_id, fname, lname):
    """
    Finds a member by academy id and member's first and last name.
    :param aca_id: academy id
    :param fname: member's first name
    :param lname: member's last name
    :return: Member object if found, otherwise, None
    """
    try:
        return Member.objects.get(aca_id=aca_id, first_name=fname,
                                last_name=lname)
    except Member.DoesNotExist:
        return None

@login_required
def check_in_success(request, **kwargs):
    """
    Displays a checked-in successful message.
    :param request:
    :param kwargs:
    :return:
    """
    return render(request, 'acagiaApp/checkin_success.html')
