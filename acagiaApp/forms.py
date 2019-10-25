from django import forms
from .models import Academy

class AcademyForm(forms.ModelForm):
    class Meta:
        model = Academy
        fields = ('aca_name', 'aca_type', 'office_phone')
