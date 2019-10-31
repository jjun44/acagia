from django import forms
from .models import Academy, Address, Member, Course
from django.forms.widgets import *

class AcademyForm(forms.ModelForm):
    aca_name = forms.CharField(
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    aca_type = forms.ChoiceField(
        choices=Academy.ACA_TYPE,
        widget=forms.Select(attrs={'class':'form-control'})
    )
    office_phone = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder':'###-###-####',
                                      'class':'form-control'})
    )

    class Meta:
        model = Academy
        fields = ('aca_name', 'aca_type', 'office_phone')

class AddressForm(forms.ModelForm):
    street = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    city = forms.CharField(
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    state = forms.ChoiceField(
        choices=Address.STATES,
        widget=forms.Select(attrs={'class':'form-control'})
    )
    zip = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class':'form-control'})
    )

    class Meta:
        model = Address
        fields = ('street', 'city', 'state', 'zip')

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('first_name', 'last_name', 'mem_type', 'date_of_birth',
                  'gender', 'cell_phone', 'email', 'img')
        labels = {
            'mem_type': 'Member Type',
            'img': 'Member Photo'
        }
        widgets = {
            'first_name': TextInput(attrs={'class':'form-control mb-2'}),
            'last_name': TextInput(attrs={'class':'form-control mb-2'}),
            'mem_type': Select(attrs={'class':'form-control mb-2'}),
            'date_of_birth': DateInput(attrs={
                'class':'form-control mb-2', 'type':'date'}),
            'gender': Select(attrs={'class':'form-control mb-2'}),
            'cell_phone': TextInput(attrs={'class':'form-control mb-2'}),
            'email': EmailInput(attrs={'class':'form-control mb-2'}),
            'img': FileInput(attrs={'class':'form-control-file mb-2'})
        }
        required = {
            'img': False,
        }
        choices = {
            'mem_type': Member.MEM_TYPE,
            'gender': Member.GENDER
        }

class CourseForm(forms.ModelForm):
    course_days = forms.MultipleChoiceField(
        choices=Course.DAYS,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'mb-2 list-unstyled'})
    )

    class Meta:
        model = Course
        fields = ('course_name', 'course_days', 'start_time',
                  'end_time', 'instructor')
        labels = {
            'course_name': 'Class Name',
            'course_days': 'Class Days'
        }
        widgets = {
            'course_name': TextInput(attrs={'class':'form-control mb-2'}),
            'start_time': TimeInput(attrs={
                'class':'form-control mb-2', 'type':'time'}),
            'end_time': TimeInput(attrs={
                'class':'form-control mb-2', 'type':'time'}),
            'instructor': Select(attrs={'class':'form-control mb-2'})
        }

    def __init__(self, *args, **kwargs):
        academy = kwargs.pop('aca_id')
        super().__init__(*args, **kwargs)
        # Show only current academy's instructors as an option
        self.fields['instructor'].queryset = Member.objects.filter(
            mem_type=Member.INST, aca_id=academy)