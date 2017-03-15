from stats.models import UserProfile, Client
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _

class UserCreationForm(UserCreationForm):
    username = forms.EmailField(widget=forms.TextInput(attrs={'maxlength':75}), label=_("Email"))
    invite_key = forms.CharField(required=True, widget=forms.TextInput(attrs={'maxlength':75, 'required': "required"}), label=_("Invite Key"))

class BootstrapModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(BootstrapModelForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


SERVICES_REQUESTED_OPTIONS = ('Victim Services, Individual Therapy, Group Therapy, Other')

class PatientIntakeForm(BootstrapModelForm):
    client_number = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Client Number'}), required=True)
    date_of_birth = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'YYYY-MM-DD'}))
    #victim_services = forms.BooleanField(widget=forms.CheckboxInput)

    OPTIONS = (
        ("VS", "Victim Services"),
        ("PH", "Placeholder")
    )
    victim_services = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(attrs={'class':'form-control'}), choices=OPTIONS)


    def __init__(self, *args, **kwargs):
        super(PatientIntakeForm, self).__init__(*args, **kwargs)
        self.fields['client_number'].label = "Client Number"
        self.fields['date_of_birth'].label = "Date of Birth"
        self.fields['victim_services'].label = "Victim Services"
        self.fields['individual_therapy'].label = "Individual Therapy"
        self.fields['group_therapy'].label = "Group Therapy"
        #if condition():
         #   self.fields['victim_services'].initial = True

    class Meta:
        model = Client
        fields = ['client_number','date_of_birth','victim_services','individual_therapy', 'group_therapy']
