from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _
from .models import UserProfile, Client, RequestedService, Referral, CurrentSituation



class UserCreationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'maxlength':75}), label=_("Username"))
    invite_key = forms.CharField(required=True, widget=forms.TextInput(attrs={'maxlength':75, 'required': "required"}), label=_("Invite Key"))

class BootstrapModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(BootstrapModelForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

class patientForm(forms.Form):
    """
    Client Info
    """
    client_number       = forms.CharField(widget=forms.TextInput(
                                            attrs={'class':'form-control'}),
                                            required=True)
    date_of_birth       = forms.DateField(widget=forms.TextInput(
                                            attrs={'class':'form-control','placeholder':'YYYY-MM-DD', 'type':'date'}))
    age                 = forms.IntegerField(required=False, label="Age at time of visit")
    number_of_abuses    = forms.IntegerField(required=False, label="Number of Abuses")

    """
    Services Provided info
    """
    victim_services     = forms.BooleanField(required=False, label="Victim Services")
    individual_therapy  = forms.BooleanField(required=False, label="Individual Therapy")
    group_therapy       = forms.BooleanField(required=False, label="Group Therapy")

    """
    Referral Info
    """
    web                 = forms.BooleanField(required=False, label="Web")
    social_service      = forms.BooleanField(required=False, label="Social Service")
    health_practitioner = forms.BooleanField(required=False, label="Health Practitioner")
    alcoholics_anonymous= forms.BooleanField(required=False, label="AA")
    drug_treatment_group= forms.BooleanField(required=False, label="Drug Treatment Group")
    advertisement       = forms.BooleanField(required=False, label="Advertisement")
    other_referral      = forms.CharField(max_length=30, required=False, label="Other")

    """
    Abuse Info
    """
    start_date          = forms.CharField(required=False, max_length = 4, label="Start Date (Year)")
    stop_date           = forms.CharField(required=False, max_length = 4, label="Stop Date (Year)")
    role_of_abuser      = forms.CharField(required=False, label="Role of Abuser")
    reported_date       = forms.CharField(required=False, max_length = 4, label="Reported Date (Year)")
    family_context      = forms.CharField(required=False, max_length = 12, label='Family Context')

    """
    Sexual Orientation Info
    """
    # Get choices from models
    sex_choices = [('','')] + CurrentSituation.sex_choices
    income_choices = [('','')] + CurrentSituation.income_choices
    edu_choices = [('','')] + CurrentSituation.edu_choices

    
    medication1         = forms.CharField(required=False, max_length=50, label="Medication 1")
    purpose1            = forms.CharField(required=False, max_length=150, label="Medication's purpose")
    medication2         = forms.CharField(required=False, max_length=50, label="Medication 2")
    purpose2            = forms.CharField(required=False, max_length=150, label="Medication's purpose")
    sexual_orientation  = forms.ChoiceField(required=False, label="Sexual Orientation", choices=sex_choices)
    income              = forms.ChoiceField(required=False, label="Income", choices=income_choices)
    level_of_education  = forms.ChoiceField(required=False, label="Level of Education", choices=edu_choices)
    profession          = forms.CharField(required=False, max_length=50, label="Profession")
    in_treatment        = forms.BooleanField(required=False, label="In treatment?")
