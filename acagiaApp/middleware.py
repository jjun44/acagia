import pytz
from django.utils import timezone

# Set the current time zone
# https://docs.djangoproject.com/en/2.2/topics/i18n/timezones/
# https://stackoverflow.com/questions/27517259/django-activate-not-showing-effect
class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tzname = request.session.get('django_timezone')
        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()
        return self.get_response(request)

