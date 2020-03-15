from django import forms
from django.forms import formset_factory
from .models import Academy, Member, Course, Attendance, Rank, MemberRank, \
    Event, PaymentTerm, MemberPayment
from django.forms.widgets import TextInput, Select, EmailInput, DateInput, \
    TimeInput, SplitDateTimeWidget, DateTimeInput, NumberInput

class AcademyForm(forms.ModelForm):
    class Meta:
        model = Academy
        fields = ('aca_name', 'aca_type', 'office_phone',
                  'location',
                  'time_zone')
        labels = {
            'aca_name': 'Academy name',
            'aca_type': 'Academy type',
            'location': 'Location (for display purpose)'
        }
        widgets = {
            'aca_name': TextInput(attrs={'class':'form-control mb-2'}),
            'aca_type': Select(attrs={'class':'form-control mb-2'}),
            'office_phone': TextInput(attrs={'placeholder':'###-###-####',
                                             'class':'form-control mb-2'}),
            'location': TextInput(attrs={'placeholder': '272 May Street, '
                                                        'San Jose, CA',
                                         'class': 'form-control mb-2'}),
        }
        choices = {
            'aca_type': Academy.ACA_TYPE,
            'time_zone': Academy.TIME_ZONES,
        }

class MemberForm(forms.ModelForm):
    # https://coderwall.com/p/bz0sng/simple-django-image-upload-to-model-imagefield
    img = forms.ImageField(
        label='Member photo',
        required = False
    )

    class Meta:
        model = Member
        fields = ('first_name', 'last_name', 'mem_type', 'date_of_birth',
                  'gender', 'cell_phone', 'email', 'address', 'img')
        labels = {
            'mem_type': 'Member type',
        }
        widgets = {
            'first_name': TextInput(attrs={'class':'form-control mb-2'}),
            'last_name': TextInput(attrs={'class':'form-control mb-2'}),
            'mem_type': Select(attrs={'class':'form-control mb-2'}),
            'date_of_birth': DateInput(attrs={
                'class':'form-control mb-2', 'type':'date'}),
            'gender': Select(attrs={'class':'form-control mb-2'}),
            'cell_phone': TextInput(attrs={'class':'form-control mb-2',
                                           'placeholder':'###-###-####'}),
            'email': EmailInput(attrs={'class':'form-control mb-2',
                                       'placeholder':'acagia@example.com'}),
            #'img': FileInput(attrs={'class':'form-control-file mb-2'})
        }
        required = {
            'address': False,
        }
        choices = {
            'mem_type': Member.MEM_TYPE,
            'gender': Member.GENDER,
        }

class MemberUpdateForm(MemberForm):
    class Meta:
        model = Member
        fields = ('first_name', 'last_name', 'status', 'mem_type',
                  'date_of_birth', 'gender', 'cell_phone', 'email',
                  'member_since', 'address', 'img')
        labels = {
            'member_since': 'Member since',
            'mem_type': 'Member type'
        }
        widgets = {
            'member_since': DateInput(attrs={'type':'date'}),
        }

class CourseForm(forms.ModelForm):
    course_days = forms.MultipleChoiceField(
        choices=Course.DAYS,
        label='Class days (select all that apply)',
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'mb-2 list-unstyled'})
    )

    class Meta:
        model = Course
        fields = ('course_name', 'course_days', 'start_time',
                  'end_time', 'instructor')
        labels = {
            'course_name': 'Class name',
            'start_time': 'Start time (e.g. 10:00 AM)',
            'end_time': 'End time (e.g. 12:00 PM)',
            'instructor': 'Instructor (not selecting will be set to '
                          '\'Not Specified\')'
        }
        widgets = {
            'course_name': TextInput(attrs={'class':'form-control mb-2'}),
            'start_time': TimeInput(format='%H:%M', attrs={
                'class':'form-control mb-2', 'type':'time'
            }),
            'end_time': TimeInput(format='%H:%M', attrs={
                'class':'form-control mb-2', 'type':'time'
            }),
            'instructor': Select(attrs={'class':'form-control mb-2'})
        }
        required = {
            'instructor': False,
        }

    def __init__(self, *args, **kwargs):
        aca_id = kwargs.pop('aca_id')
        super().__init__(*args, **kwargs)
        # Show only current academy's instructors as an option
        self.fields['instructor'].queryset = Member.objects.filter(
            mem_type=Member.INST, aca_id=aca_id)

    def clean_course_days(self):
        """
        Formats course_days e.g. ['M', 'W', 'F'] -> M/W/F before saving.
        :return:
        """
        # Format course days
        course_days = self.cleaned_data['course_days']
        formatted_days = ''
        for day in course_days:
            formatted_days += day + '/'
        # Remove the last '/' ch
        return formatted_days[0:len(formatted_days) - 1]

class CheckInForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder':'First Name',
                                      'class':'form-control form-control-lg'})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder':'Last Name',
                                      'class':'form-control form-control-lg'})
    )

    class Meta:
        model = Attendance
        fields = ('course',)
        widgets = {
            'course': Select(attrs={'class':'form-control mb-2'})
        }

    def __init__(self, *args, **kwargs):
        aca_id = kwargs.pop('aca_id')
        super().__init__(*args, **kwargs)
        # Show only current academy's courses as an option
        self.fields['course'].queryset = Course.objects.filter(aca_id=aca_id)

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ('date_attended', 'time_attended', 'member', 'course')
        widgets = {
            'date_attended': DateInput(attrs={'type': 'date'}),
            'time_attended': TimeInput(format='%H:%M', attrs={
                'type':'time'})
        }

    def __init__(self, *args, **kwargs):
        aca_id = kwargs.pop('aca_id')
        super().__init__(*args, **kwargs)
        self.fields['member'].queryset = Member.objects.filter(aca_id=aca_id)
        self.fields['course'].queryset = Course.objects.filter(aca_id=aca_id)

class AttendanceDateForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ('date_attended',)
        widgets = {
            'date_attended': DateInput(attrs={'type': 'date'})
        }
        labels = {
            'date_attended': ''
        }

class MemberRankForm(forms.ModelForm):
    class Meta:
        model = MemberRank
        fields = ('rank', 'days_attended', 'days_left', 'total_days')

    def __init__(self, *args, **kwargs):
        aca_id = kwargs.pop('aca_id')
        super().__init__(*args, **kwargs)
        self.fields['rank'].queryset = Rank.objects.filter(
            aca_id=aca_id).order_by('rank_order')

class RankForm(forms.ModelForm):
    class Meta:
        model = Rank
        fields = ('rank_order', 'rank', 'days_required')
        widgets = {
            'rank_order': TextInput(attrs={
                'placeholder':'e.g. 1',
                'class':'form-control'
            }),
            'rank': TextInput(attrs={
                'placeholder': 'Enter rank name e.g. White',
                'class':'form-control'
            }),
            'days_required': TextInput(attrs={
                'placeholder': 'e.g. 30',
                'class': 'form-control'
            }),
        }

# https://docs.djangoproject.com/en/2.2/topics/forms/formsets/
# https://medium.com/all-about-django/adding-forms-dynamically-to-a-django-formset-375f1090c2b0
RankFormset = formset_factory(RankForm, extra=1)

'''
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('title', 'start_time', 'end_time', 'description')
        widgets = {
            'start_time': DateInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'end_time': DateInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
        }

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        # Parse HTML5 datetime-local input to datetime field
        self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)
'''

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('title', 'start_date', 'end_date', 'start_time',
                  'end_time', 'credit', 'notes')
        labels = {
            'start_time': 'Start time (set to All Day if not specified)',
            'credit': 'Attendance credit'
        }
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
            'start_time': TimeInput(attrs={'type': 'time'},
                                    format='%H:%M'),
            'end_time': TimeInput(attrs={'type': 'time'},
                                  format='%H:%M')
        }

class PaymentTermForm(forms.ModelForm):
    class Meta:
        model = PaymentTerm
        fields = ('term_name', 'amount', 'n_month', 'install_factor',
                  'discount')
        labels = {
            'n_month': 'Every n month of payment',
            'install_factor': 'Number of months to divide the amount',
            'discount': 'Discount in %'
        }
        widgets = {
            'term_name': TextInput(attrs={'placeholder':
                                              '1-year-installation'}),
            'amount': NumberInput(attrs={'placeholder': 1800}),
            'n_month': NumberInput(attrs={'placeholder': 1}),
            'install_factor': NumberInput(attrs={'placeholder': 12}),
            'discount': NumberInput(attrs={'placeholder': 10})
        }

class MemberPaymentAddForm(forms.ModelForm):
    class Meta:
        model = MemberPayment
        fields = ('pay_status', 'nth_day', 'pay_term')
        labels = {
            'pay_status': 'Payment status',
            'nth_day': 'Enter nth day of month for recurring payments',
            'pay_term': 'Payment option'
        }
        widgets = {
            'nth_day': NumberInput(attrs={'placeholder': 'e.g. enter 5 for '
                                                          '5th, 24 for 24th'})
        }

        def __init__(self, *args, **kwargs):
            aca_id = kwargs.pop('aca_id')
            super().__init__(*args, **kwargs)
            # Show only current academy's payment terms as an option
            self.fields['pay_term'].queryset = PaymentTerm.objects.filter(aca_id=aca_id)

class MemberPaymentUpdateForm(MemberPaymentAddForm):
    class Meta:
        model = MemberPayment
        fields = ('pay_status', 'nth_day', 'pay_term', 'late_fee', 'month_count')
        labels = {
            'pay_status': 'Payment status',
            'nth_day': 'Enter nth day of month for recurring payments',
            'pay_term': 'Payment option',
            'month_count': 'Number of months left for the next recurring ' \
                           'payment'
        }
