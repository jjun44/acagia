# ----------------------------------------------------------------------
# Name:        courses
# Purpose:     Handles requests for managing courses
#
# Date:        11/1/2019
# ----------------------------------------------------------------------
"""
Handles requests for managing courses.
"""

from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView, DeleteView
from acagiaApp.forms import CourseForm
from acagiaApp.models import Course

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
        ).order_by("start_time", "end_time")
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
