from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _
from .models import UserProfile, Client, ServicesRequested, Referral


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

class patientForm(forms.Form):
    """ 
    Client Info
    """
    client_number       = forms.CharField(widget=forms.TextInput(
                                            attrs={'class':'form-control','placeholder':'Client Number'}), 
                                            required=True)
    date_of_birth       = forms.CharField(widget=forms.TextInput(
                                            attrs={'class':'form-control','placeholder':'YYYY-MM-DD'}))
    age                 = forms.IntegerField(required=False)
    number_of_abuses    = forms.IntegerField(required=False)

    """
    Services Provided info
    """
    victim_services     = forms.BooleanField(required=False)         
    individual_therapy  = forms.BooleanField(required=False)      
    group_therapy       = forms.BooleanField(required=False)     

    """
    Referral Info
    """
    web                 = forms.BooleanField(required=False)
    social_service      = forms.BooleanField(required=False)
    health_practitioner = forms.BooleanField(required=False)
    alcoholics_anonymous= forms.BooleanField(required=False)
    drug_treatment_group= forms.BooleanField(required=False)
    advertisement       = forms.BooleanField(required=False)
    other_referral      = forms.CharField(max_length=30, required=False)

    """
    Abuse Info
    """
    start_date          = forms.CharField( max_length = 3)
    stop_date           = forms.CharField( max_length = 3)
    role_of_abuser      = forms.IntegerField()
    reported_date       = forms.CharField( max_length = 3)
    family_context      = forms.CharField( max_length = 12)

    """
    Sexual Orientation Info
    """
    medication1         = forms.CharField(max_length=50)
    purpose1            = forms.CharField(max_length=150)
    medication2         = forms.CharField(max_length=50)
    purpose2            = forms.CharField(max_length=150)
    sexual_orientation  = forms.IntegerField()
    income              = forms.IntegerField()
    level_of_education  = forms.IntegerField()
    profession          = forms.CharField(max_length=50)
    in_treatment        = forms.BooleanField()



    

    
class PatientIntakeForm(BootstrapModelForm):
    client_number = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Client Number'}), required=True)
    date_of_birth = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'MM/DD/YYYY'}))
    #health_professionals = forms.BooleanField(required=True)

    def __init__(self, *args, **kwargs):
        super(PatientIntakeForm, self).__init__(*args, **kwargs)
        self.fields['client_number'].label = "Client Number"
        self.fields['date_of_birth'].label = "Date of Birth"
        #self.fields['health_professionals'].label = "In treatment with other health professionals?"

    class Meta:
        model = Client
        fields = ['client_number','date_of_birth']

class ServicesRequiredForm(BootstrapModelForm):
    victim_services = forms.BooleanField(required=False, label="Victim Services")
    individual_therapy = forms.BooleanField(required=False, label="Individual Therapy")
    group_therapy = forms.BooleanField(required=False, label="Group Therapy")

    def __init__(self, *args, **kwargs):
        super(ServicesRequiredForm, self).__init__(*args, **kwargs)
        self.fields['victim_services'].label = "Victim Services"
        self.fields['individual_therapy'].label = "Individual Therapy"
        self.fields['group_therapy'].label = "Group Therapy"

    class Meta:
        model = ServicesRequested
        exclude = ['client1']

class ReferredByForm(BootstrapModelForm):
    web = forms.BooleanField(initial=False, required=False)
    social_service = forms.BooleanField(initial=False, required=False)
    health_practitioner = forms.BooleanField(initial=False, required=False)
    alcoholics_anonymous = forms.BooleanField(initial=False, required=False)
    drug_treatment_group = forms.BooleanField(initial=False, required=False)
    advertisement = forms.BooleanField(initial=False, required=False)
    other1 = forms.BooleanField(initial=False, required=False)
    other2 = forms.CharField(max_length=30, required=False)

    def __init__(self, *args, **kwargs):
        super(ReferredByForm, self).__init__(*args, **kwargs)
        self.fields['web'].label = "Web"
        self.fields['social_service'].label = "Social Service"
        self.fields['health_practitioner'].label = "Health Practitioner"
        self.fields['alcoholics_anonymous'].label = "Alcoholics Anonymous"
        self.fields['drug_treatment_group'].label = "Drug Treatment Group"
        self.fields['advertisement'].label = "Advertisement"
        self.fields['other2'].label = "Other"

    class Meta:
        model = Referral
        exclude = ['client1']