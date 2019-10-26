from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from users.models import CustomUser as User
from .forms import AcademyForm, AddressForm
from .models import Academy, Member, Attendance
from datetime import date


@login_required(login_url='login_error')
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
                  {'academy':academy, 'num_stu':num_of_students,
                   'num_att':num_of_attended})

@login_required(login_url='login_error')
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

@method_decorator(login_required(login_url='login_error'),
                  name='dispatch')
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