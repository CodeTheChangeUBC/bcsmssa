from django.utils.crypto import get_random_string
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import login as view_login
from django.contrib.auth import authenticate, login as auth_login
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.views.generic.edit import CreateView, UpdateView
from .forms import patientForm, UserCreationForm
from .models import InviteKey, Client, Abuse, CurrentSituation, RequestedService, Referral
from .helpers import create_models, charts, basic_stats
import json
from django.contrib import messages



@login_required
def statistics(request):
    graphs = charts()
    stats = basic_stats()
    return render(request, 'stats/statistics.html', {**graphs, **stats})

@login_required
def data(request):
    # Load data for relevant tables
    data = {}
    data['clients']         = Client.objects.all()
    data['client_fields']   = Client._meta.get_fields()[5:]
    data['services']        = RequestedService.objects.all()
    data['service_fields']  = RequestedService._meta.get_fields()[0:]
    data['referrals']       = Referral.objects.all()
    data['referral_fields'] = Referral._meta.get_fields()[0:]
    data['abuses']          = Abuse.objects.all()
    data['abuse_fields']    = Abuse._meta.get_fields()[2:]
    data['situations']      = CurrentSituation.objects.all()
    data['sitch_fields']    = CurrentSituation._meta.get_fields()[1:]

    return render(request, 'stats/data.html', data)

@login_required
def form(request):
    data = {}
    if request.method == "POST":
        form = patientForm(request.POST)
        if form.is_valid():
            num_occurrences = Client.objects.filter(client_number=form.cleaned_data['client_number']).count()
            print(num_occurrences)
            if num_occurrences > 0: 
                messages.warning(request, 'Client number already taken.')
            else: 
                create_models(form)
                # Render success message and generate blank form
                messages.success(request, 'Client intake successful!')
                return redirect('/form')
        else:
            messages.warning(request, 'Oops, something went wrong.')
    else:
        form = patientForm()
        
    fields = list(form)
    data['form'] = form
    data['referral_info']           = fields[7:14]
    data['services_provided']       = fields[4:7]
    data['abuse_info']              = fields[14:19]
    data['sexual_orientation_info'] = fields[19:]

    return render(request, 'stats/form_features.html', data)



@login_required
def profile(request):
    data = {}

    # Send list of keys and users to front end if the request came from the admin
    if request.user.is_superuser:
        keys = InviteKey.objects.all()
        data['keys'] = keys
        data['users'] = User.objects.all()

    return render(request, 'stats/profile.html', data)

def get_user_profile(request, username):
    # If the requested profile is the currently logged in user then just
    # redirect to their personal profile page
    if request.user.username == username:
        return redirect('/profile')

    # Get the requested user from the data base and send that info to the
    # user_profile template
    data = {}
    user = User.objects.get(username=username)
    data['user'] = user
    return render(request, 'stats/user_profile.html', data)

def get_client_info(request, client_number):
    # Get the requested client from the data base and send that info to the
    # client_info template
    data = {}
    client = Client.objects.get(client_number=client_number)
    data['client'] = client
    return render(request, 'stats/client_info.html', data)




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



# Handles registration http requests
def user_register(request):
    # Redirect to homepage if logged in already
    if request.user.is_authenticated():
        return redirect(settings.LOGIN_REDIRECT_URL)

    # Handle registration form submission
    if request.method == "POST":
        valid_key = False
        form = UserCreationForm(data=request.POST)

        # Must call .is_valid() to access cleaned_data
        if form.is_valid():
            key = form.cleaned_data['invite_key']

            if InviteKey.objects.filter(id=key).exists():
                InviteKey.objects.filter(id=key).delete()
                user = form.save()
                user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
                auth_login(request, user)
                return HttpResponseRedirect('/')
            else:
                form.add_error('invite_key', 'The provided key is not valid.')
        else:
            # Print errors if some field is wrong (shows erros in html too)
            print(form.errors)
    else:
        # Show form by default
        form = UserCreationForm()

    return render(request, 'stats/register.html', {'form': form })


# List of all clients
@login_required
def clients(request):
    data = {}
    data['clients']         = Client.objects.all()
    data['client_fields']   = Client._meta.get_fields()[5:]
    data['service_fields']  = RequestedService._meta.get_fields()[0:]
    data['referral_fields'] = Referral._meta.get_fields()[0:]
    data['abuse_fields']    = Abuse._meta.get_fields()[2:]
    data['sitch_fields']    = CurrentSituation._meta.get_fields()[1:]

    return render(request, 'stats/clients.html', data)

# Client Update view
class ClientUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Client
    fields = [f.name for f in Client._meta.get_fields()[3:]]
    template_name = 'stats/updates/client_edit.html'
    success_url = '/clients'
    success_message = "Client Updated was updated successfully!"



# Use Django's built in login system but redirect to the homepage if already
# logged in
def user_login(request, **kwargs):
    if request.user.is_authenticated():
        return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        return view_login(request, **kwargs)
