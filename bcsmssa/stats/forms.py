from stats.models import UserProfile
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _

class UserCreationForm(UserCreationForm):
    username = forms.EmailField(widget=forms.TextInput(attrs={'maxlength':75}), label=_("Email"))
    invite_key = forms.CharField(required=True, widget=forms.TextInput(attrs={'maxlength':75, 'required': "required"}), label=_("Invite Key"))
