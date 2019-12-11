# ----------------------------------------------------------------------
# Name:        members
# Purpose:     Handles requests for managing members
#
# Date:        10/26/2019
# ----------------------------------------------------------------------
"""
Handles requests for managing members.
"""

from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DeleteView
from acagiaApp.forms import MemberForm, MemberUpdateForm
from acagiaApp.models import Member, MemberRank
from django.utils import timezone

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