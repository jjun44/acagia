from django import forms
from .models import Academy, Member, Course, Attendance
from django.forms.widgets import *

class AcademyForm(forms.ModelForm):
    class Meta:
        model = Academy
        fields = ('aca_name', 'aca_type', 'office_phone', 'location', 'time_zone')
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
                                         'class': 'form-control mb-2'})
        }
        choices = {
            'aca_type': Academy.ACA_TYPE,
            'time_zone': Academy.TIME_ZONES,
        }

'''
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('street', 'city', 'state', 'zip')
        widgets = {
            'street': TextInput(attrs={'class':'form-control mb-2'}),
            'city': TextInput(attrs={'class':'form-control mb-2'}),
            'state': Select(attrs={'class':'form-control mb-2'}),
            'zip': TextInput(attrs={'class':'form-control mb-2'})
        }
        choices = {
            'state': Address.STATES,
        }
'''

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
            'gender': Member.GENDER
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
        Formats course_days e.g. ['M', 'W', 'F'] -> M/W/F.
        :return:
        """
        # Format and save course days
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
            'time_attended': TimeInput(format='%H:%M:%S'),
            'course': Select(attrs={'class':'form-control mb-2'})
        }

    def __init__(self, *args, **kwargs):
        aca_id = kwargs.pop('aca_id')
        super().__init__(*args, **kwargs)
        # Show only current academy's courses as an option
        self.fields['course'].queryset = Course.objects.filter(aca_id=aca_id)

