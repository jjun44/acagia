from django.db.models.signals import pre_save
from django.dispatch import receiver
from acagiaApp.models import MemberRank, Rank
from acagiaApp.views import promotion


@receiver(pre_save, sender=MemberRank)
def update_member_rank(sender, instance, update_fields, **kwargs):
    # Get original obj before saving new changes to compare
    pre_rank = MemberRank.objects.get(id=instance.id)
    # Handle when rank changed (by promotion or manually)
    if instance.rank != pre_rank.rank:
        print('rank changed')
        instance.days_attended = 0
        instance.days_left = instance.rank.days_required
        #promotion.reset_days(instance)
    # Handle when days attended changed (event credit, check-in, or manually)
    elif instance.days_attended != pre_rank.days_attended:
        print('days changed')
        # If days_attended increased, than the total days
        # needs to be smaller.
        pre_sum = pre_rank.total_days - pre_rank.days_attended
        post_sum = instance.total_days - instance.days_attended
        # If days_attended increased, adjust others accordingly
        if pre_sum > post_sum:
            increased_amt = instance.days_attended - pre_rank.days_attended
            instance.days_left -= increased_amt
            instance.total_days += increased_amt
        # days_attended decreased
        else:
            decreased_amt = pre_rank.days_attended - instance.days_attended
            instance.days_left += decreased_amt
            instance.total_days -= decreased_amt







