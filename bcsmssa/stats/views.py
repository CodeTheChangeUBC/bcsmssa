from django.utils.crypto import get_random_string
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from stats.models import InviteKey
from stats.forms import MyRegistrationForm
from django.contrib.auth.views import login as contrib_login
from django.conf import settings
import json

@login_required
def profile(request):
    # Send list of users to front end if the request came from the admin
    if request.user.is_superuser:
        users = User.objects.all()
        keys = InviteKey.objects.all()
        data = {'users':users, 'keys':keys}
        return render(request, 'stats/profile.html', data)

    # Return regular page if not an admin request
    return render(request, 'stats/profile.html', {})

@login_required
def homepage(request):
    return render(request, 'stats/homepage.html', {})

@login_required
def form(request):
    return render(request, 'stats/form.html', {})

@login_required
def invite_key(request):
    # Only admin can create new invite keys
    if request.user.is_superuser:

        # Handle a POST request, creates a new key
        if request.method == 'POST':
            # Only allow a maximum of 10 active invitation keys
            if InviteKey.objects.all().count() < 10:
                new_key = InviteKey(id = get_random_string(length=6))
                new_key.save();
                data = { 'success': True, 'key': new_key.id }
                return JsonResponse(data)
            else:
                data = { 'success': False}
                return JsonResponse(data)

        # Handle a DELETE request, deletes a specified key
        if request.method == 'DELETE':
            # Get key data
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            key_value = body['key_value']
            InviteKey.objects.filter(id=key_value).delete()
            data = { 'success': True, 'key': key_value}
            return JsonResponse(data)

    # Return bad request error if http request was not POST
    return HttpResponseBadRequest()


def register(request):
    if request.user.is_authenticated():
        return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        if request.method == 'POST':
            form = MyRegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect(settings.LOGIN_REDIRECT_URL)

        form = MyRegistrationForm()

        return render(request, 'stats/register.html', {'form': form})

def login(request, **kwargs):
    if request.user.is_authenticated():
        return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        return contrib_login(request, **kwargs)
