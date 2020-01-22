from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from acagiaApp.forms import RankForm, PaymentTermForm
from acagiaApp.models import Academy, PaymentTerm, MemberPayment
from django.contrib import messages
from django.db import IntegrityError


@method_decorator(login_required, name='dispatch')
class PaySystemListView(ListView):
    """
    Shows the list of payment system customized by the user.
    """
    model = PaymentTerm
    template_name = 'acagiaApp/payment_system_list.html'

    def get_context_data(self, **kwargs):
        aca_id = self.request.session['aca_id']
        context = super().get_context_data(**kwargs)
        # Get all the payment terms associated with the academy
        terms = PaymentTerm.objects.filter(aca_id=aca_id).order_by(
            'amount', 'term_name').defer('id', 'aca_id')
        context['terms'] = terms
        context['academy'] = Academy.objects.get(
            id=aca_id)
        return context

@method_decorator(login_required, name='dispatch')
class PayTermCreateView(CreateView):
    """
    Adds a new payment term.
    """
    model = PaymentTerm
    form_class = PaymentTermForm
    template_name = 'acagiaApp/payterm_form.html'
    success_url = reverse_lazy('pay_sys_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.aca_id = self.request.session['aca_id']
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['template'] = {'action_name': 'Add New Payment Term',
                               'btn_name':
            'Add Term'}
        return context

@method_decorator(login_required, name='dispatch')
class PayTermDeleteView(DeleteView):
    """
    Deletes selected rank information and redirects to the rank system page.
    """
    model = PaymentTerm

    def get_success_url(self):
        return reverse('pay_sys_list')

@method_decorator(login_required, name='dispatch')
class PayTermUpdateView(UpdateView):
    """
    Updates existing payment term information.
    """
    model = PaymentTerm
    form_class = PaymentTermForm
    success_url = reverse_lazy('pay_sys_list')
    template_name = 'acagiaApp/payterm_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['template'] = {'action_name': 'Update Payment Term',
                               'btn_name':
            'Update'}
        return context