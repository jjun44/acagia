# ----------------------------------------------------------------------
# Name:        promotion
# Purpose:     Handles requests for ranking and promotion systems
#
# Date:        11/6/2019
# ----------------------------------------------------------------------
"""
Handles requests for ranking and promotion systems.
"""

from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView, DeleteView
from acagiaApp.forms import RankFormset, RankForm, MemberRankForm
from acagiaApp.models import Academy, Rank, MemberRank
from django.contrib import messages
from django.db import IntegrityError

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
    # If no rank system is made, sends an error message and
    # redirect the user to make one.
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
            current = 'New Member'
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
                pre = ''
                next = ''
            elif current == first_rank: # Member is at first rank
                pre = ''
                next = all_ranks.filter(
                    rank_order__gt=member.rank.rank_order).first()
            elif current == last_rank: # Member is at last rank
                pre = all_ranks.filter(
                    rank_order__lt=member.rank.rank_order).last()
                next = ''
            else:
                pre = all_ranks.filter(
                    rank_order__lt=member.rank.rank_order).last()
                next = all_ranks.filter(
                    rank_order__gt=member.rank.rank_order).first()

        if current == 'New Member' or next == '':
            member.days_left = ''
        else:
            member.days_left = member.days_left
        # if current is set to X, calculate days left with 0
        mem_rank = {'id': member.id, 'name': member.member, 'pre': pre,
                    'current': current, 'next': next, 'days_left':
                        member.days_left, 'photo': member.member.img
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
    print(selected_ids)
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
        else: # Assign correct rank
            success_msg += str(member.member) + ', '
            if operation == 'promote':
                member.rank = next
            else:
                member.rank = pre
            num_success += 1
            #reset_days(member)
            member.save()

    # Send successful message if 1 or more members are promoted
    if num_success > 0:
        messages.success(request, str(num_success) + success_msg[0:-2])
    # Send fail message if 1 or more members are failed to be promoted
    if num_fail > 0:
        messages.error(request, str(num_fail) + fail_msg[0:-2])

def reset_days(member):
    """
    Resets member's days attended at the current rank to 0
    and days left to the same as the current rank's required days
    when he/she gets promoted or demoted (whenever rank changes).
    :param member: (MemberRank) given member's rank object
    """
    member.days_attended = 0
    member.days_left = member.rank.days_required

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


