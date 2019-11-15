from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Event

class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    def formatday(self, day, events):
        """
        Formats a day as a table column and filters events by day.
        :param day:
        :param events:
        :return:
        """
        events_per_day = events.filter(start_time__day=day)
        d = ''
        for event in events_per_day:
            d += f'<li> {event.title} </li>'

        if day != 0:
            return f'<td><span class="date">{day}</span><ul> {d} </ul></td>'

        return '<td></td>'

    def formatweek(self, theweek, events):
        """
        Formats a week as a table row.
        :param theweek:
        :param events:
        :return:
        """
        week = ''
        for day, weekday in theweek:
            week += self.formatday(day, events)
        return f'<tr> {week} </tr>'

    def formatmonth(self, withyear=True):
        """
        Formats a month as a table and filters events by year and month.
        :param withyear:
        :return:
        """
        events = Event.objects.filter(start_time__year=self.year,
                                      start_time__month=self.month)
        e = Event.objects.all().first()
        print(events, e, e.start_time.year, e.start_time.month, self.year,
              self.month)
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal



