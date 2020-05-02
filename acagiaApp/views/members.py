# ----------------------------------------------------------------------
# Name:        members
# Purpose:     Handles requests for managing members
#
# Date:        10/26/2019
# ----------------------------------------------------------------------
"""
Handles requests for managing members.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DeleteView
from acagiaApp.forms import MemberForm, MemberUpdateForm, \
    MemberPaymentAddForm, MemberPaymentUpdateForm
from acagiaApp.models import Member, MemberRank, PaymentTerm, MemberPayment,\
    Rank
from django.utils import timezone
from django.contrib import messages

@login_required
def member_list(request):
    """
    Shows the list of members in the academy with basic information.
    :param request: HTTP request
    :param kwargs: keyword arguments including academy id
    :return: member list page
    """
    aca_id = request.session['aca_id']
    # If no payment system is made, redirect the user to make one
    if not PaymentTerm.objects.filter(aca_id=aca_id):
        messages.info(request, 'Make your payment system first to use '
                               'MEMBER tab now!')
        return redirect('/academy/pay-sys/')
    # If no rank system is made, redirect the user to make one
    if not Rank.objects.filter(aca_id=aca_id):
        messages.info(request, 'Make your ranking system first to use '
                               'PROMOTION tab now!')
        return redirect('/academy/rank-sys/')

    # Get current academy's members
    member_list = Member.objects.filter(
        aca_id=aca_id
    ).order_by('first_name')

    return render(request, 'acagiaApp/member_list.html',
                  {'members': member_list})

'''
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
'''

@login_required
def add_member(request):
    """
    Adds a new member.
    """
    form = MemberForm()
    pay_form = MemberPaymentAddForm()
    template_name = 'acagiaApp/member_form.html'
    template = {'action_name': 'Add New Member', 'btn_name': 'Add Member'}
    aca_id = request.session['aca_id']
    if request.method == 'POST':
        form = MemberForm(request.POST)
        pay_form = MemberPaymentAddForm(request.POST)
        if form.is_valid() and pay_form.is_valid():
            member = form.save(commit=False)
            member.aca_id = aca_id
            member.member_since = timezone.localdate()
            print(member.img)
            member.save()
            # Give a default rank to a member
            default_rank = Rank.objects.filter(aca_id=aca_id).order_by(
                'rank_order').first()
            member_rank = MemberRank(member_id=member.id,
                                     aca_id=aca_id)
            member_rank.rank = default_rank
            member_rank.days_left = default_rank.days_required
            member_rank.save()
            # Save payment information
            pay_form = pay_form.save(commit=False)
            pay_form.member_id = member.id
            pay_form.save()

            return redirect('/academy/members/')
    return render(request, template_name, {'form': form, 'pay_form':
        pay_form, 'template': template})


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

'''
@method_decorator(login_required, name='dispatch')
class MemberUpdateView(UpdateView):
    """
    Updates existing member information.
    """
    model = Member
    form_class = MemberUpdateForm
    #second_form_class = MemberPaymentUpdateForm
    success_url = reverse_lazy('mem_list')
    template_name = 'acagiaApp/member_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['mem_form'] = context['form']
        #context['pay_form'] = self.second_form_class(instance=self.object)
        context['template'] = {'action_name': 'Update Member', 'btn_name':
            'Update'}
        return context
    #
    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        mem_form = self.form_class
        pay_form = self.second_form_class
        return self.render_to_response(self.get_context_data(
            object=self.object, mem_form=mem_form, pay_form=pay_form))
    #
'''

@login_required
def update_member(request, **kwargs):
    template_name = 'acagiaApp/member_form.html'
    template = {'action_name': 'Update Member', 'btn_name': 'Update Member'}
    # https://www.geeksforgeeks.org/update-view-function-based-views-django/
    mem_id = kwargs['pk']
    # Fetch objects related to passed member id
    mem_obj = get_object_or_404(Member, id=mem_id)
    pay_obj = get_object_or_404(MemberPayment, member_id=mem_id)
    # Pass objects as instance in forms
    form = MemberUpdateForm(request.POST or None, instance=mem_obj)
    pay_form = MemberPaymentUpdateForm(request.POST or None, instance=pay_obj)

    if form.is_valid() and pay_form.is_valid():
        form.save()
        pay_form.save()
        return redirect(reverse('mem_detail', args=[mem_id]))

    context = {}
    context['form'] = form
    context['pay_form'] = pay_form
    context['template'] = template

    return render(request, template_name, {'form': form, 'pay_form':
        pay_form, 'template': template})

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