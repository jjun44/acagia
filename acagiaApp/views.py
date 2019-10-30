from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from users.models import CustomUser as User
from .forms import AcademyForm, AddressForm, MemberForm, CourseForm
from .models import Academy, Member, Attendance, Student, Course
from datetime import date

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
            academy.user_id = request.user.id
            academy.addr_id = address.id
            academy.save()
            #print("New Academy added")
            return redirect('/academy')
        #else:
            #print("Academy couldn't be added")
            #print(aca_form.errors, '\n', addr_form.errors)

    return render(request, 'acagiaApp/academy_form.html', {
        'aca_form': aca_form,
        'addr_form': addr_form
    })

@login_required
def dashboard(request, **kwargs):
    """
    Display a chosen user's academy's dashboard with
    the academy information on the page including # of students
    and # of students attended today.
    :param request: HTTP request
    :param kwargs: keyword arguments
    :return: dashboard page with academy information
    """
    academy = Academy.objects.get(id=kwargs['pk'])
    num_of_students = Member.objects.filter(aca_id=kwargs['pk']).count()
    num_of_attended = Attendance.objects.filter(
        aca_id=kwargs['pk'], date_attended=date.today()).count()
    return render(request, 'acagiaApp/dashboard.html',
                  {'academy': academy, 'num_stu': num_of_students,
                   'num_att': num_of_attended})

@login_required
def member_list(request, **kwargs):
    """
    Shows the list of members in the academy with basic information.
    """
    member_list = Member.objects.filter(
        aca_id=kwargs['pk']
    )
    return render(request, 'acagiaApp/member_list.html',
                  {'members': member_list,
                   'aca_id': kwargs['pk']})

@login_required
def add_member(request, **kwargs):
    '''
    Adds a new member to Member/Student tables.
    :param request: HTTP request
    :param kwargs:
    :return: member list page if member is added successfully,
             otherwise, form page to prompt the user member information
    '''
    mem_form = MemberForm()
    if request.method == 'POST':
        mem_form = MemberForm(request.POST)
        if mem_form.is_valid():
            member = mem_form.save(commit=False)
            member.aca_id = kwargs['pk'] # Save aca_id
            member.save()
            # if it's a student, add to the Student table too
            if member.mem_type == Member.STU:
                # Create student object with mem_id
                student = Student.create(member.id)
                student.save()
            return redirect('/academy/members/' + str(kwargs['pk']))
    return render(request, 'acagiaApp/member_form.html', {
        'form': mem_form, 'aca_id': kwargs['pk']
    })

@method_decorator(login_required, name='dispatch')
class CourseListView(ListView):
    """
    Shows the list of courses in the academy.
    """
    model = Course
    template_name = 'acagiaApp/course_list.html'

    def get_context_data(self, **kwargs):
        print(self.kwargs)
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.filter(
            aca_id=self.kwargs['pk']
        )
        context['aca_id'] = self.kwargs['pk']
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
    '''
    Adds a new course to the course table.
    :param request: HTTP request
    :param kwargs:
    :return:
    '''
    # Pass aca_id to the form.
    # https://stackoverflow.com/questions/28653699/passing-request-object-from-view-to-form-in-django
    pk = kwargs['pk']
    form = CourseForm(aca_id=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, aca_id=pk)
        if form.is_valid():
            course = form.save(commit=False)
            # Save instructor's id
            course.aca_id = pk
            course.instructor_id = form.cleaned_data['instructor'].id
            form.save()
            return redirect('/academy/courses/' + str(pk))
    return render(request, 'acagiaApp/course_form.html',
                      {'form': form, 'aca_id': pk})