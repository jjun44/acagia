from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .forms import AcademyForm
from users.models import CustomUser as User
from .models import Academy, Address

def add_academy(request, **kwargs):
    form = AcademyForm()
    user = User.objects.get(id=kwargs['pk'])
    if request.method == 'POST':
        if form.is_valid():

            form.save()
        return redirect('/academy')
    return render(request, 'acagiaApp/academy_form.html', {'form':form,
                                                           'user':user})

@method_decorator(login_required(login_url='login_error'),
                  name='dispatch')
class AcademyCreateView(CreateView):
    model = Academy
    success_url = reverse_lazy('home')
    template_name = 'acagiaApp/academy_form.html'

@method_decorator(login_required(login_url='login_error'),
                  name='dispatch')
class AcademyListView(ListView):
    model = Academy
    template_name = 'acagiaApp/academy_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['academy_list'] = Academy.objects.filter(
            user_id=self.request.user.id
        )
        return context

