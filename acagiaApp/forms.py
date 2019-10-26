from django import forms
from .models import Academy, Address

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

