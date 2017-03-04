from django.contrib.auth.forms import UserCreationForm
from django.views.decorators import csrf
from django.contrib.auth.models import User
from django import forms


class MyRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = {'email', 'password1', 'password2'}

    def save(self, commit=True):
        user = super(MyRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.name = self.cleaned_data['first_name']

        if commit:
            user.save()

        return user
