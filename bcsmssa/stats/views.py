from django.utils.crypto import get_random_string
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import login as view_login
from django.contrib.auth import authenticate, login as auth_login
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.views.generic.edit import CreateView
from .forms import patientForm
from .models import InviteKey, Client, Abuse, Client_Current_Situation as Ccs
from .helpers import create_models
import json
from graphos.sources.simple import SimpleDataSource
from graphos.renderers.gchart import LineChart



@login_required
def homepage(request):
    users = User.objects.all()
    data = {'users':users}
    return render(request, 'stats/homepage.html', data)

@login_required
def statistics(request):
    data = {}
    data['client_count'] = Client.objects.all().count()
    data['abuse_count'] = Abuse.objects.all().count()
    data['ccs_count'] = Ccs.objects.all().count()
    data['client_numbers'] = Client.objects.values('client_number')
    tempdata =  [
        ['Year', 'Sales', 'Expenses'],
        [2004, 1000, 400],
        [2005, 1170, 460],
        [2006, 660, 1120],
        [2007, 1030, 540]
    ]   
    # DataSource object
    data_source = SimpleDataSource(data=tempdata)
    # Chart object
    chart = LineChart(data_source,options={'title': "test stat plot", 
                     'hAxis': {'title': 'XXXX (xx)'},
        'vAxis': {'title': 'YYYY (yy)'},
      })
    data['chart'] = chart

    return render(request, 'stats/statistics.html', data)

@login_required
def form(request):
    data = {}
    # if request.method == 'POST':
    #     form = PatientIntakeForm(data=request.POST)
    #
    #     if form.is_valid():
    #         client = form.save()
    #         request.session['temp_data'] = client.client_number
    #         return redirect(request.META['HTTP_REFERER'], request.session['temp_data'])
    #     else:
    #         print(form.errors)
    # else:
    #     if 'temp_data' in request.session:
    #         data['previous_success'] = True
    #         data['c_num'] = request.session['temp_data']
    #     form = PatientIntakeForm()
    # data['form'] = form
    #
    # return render(request, 'stats/form.html', data)

    # if request.method == 'POST':
    #     form = PatientIntakeForm(data=request.POST)
    #     form2 = ServicesRequiredForm(data=request.POST)     #added
    #     form3 = ReferredByForm(data=request.POST)           #added
    #     print(request.POST)

    #     if all((form.is_valid(), form2.is_valid(), form3.is_valid())):
    #         client = form.save()
    #         services_required = form2.save(commit=False)
    #         referred_by = form3.save(commit=False)

    #     # are the checkboxes selected:
    #         if not request.POST.get("Individual Therapy", None) == None:
    #             services_required.individual_therapy += 1
    #         if not request.POST.get("Victim Services", None) == None:
    #             services_required.victim_services += 1
    #         if not request.POST.get("Group Therapy", None) == None:
    #             services_required.group_therapy += 1
    #         if not request.POST.get("Web", None) == None:
    #             referred_by.web = True
    #         if not request.POST.get("Social Service", None) == None:
    #             referred_by.social_service = True
    #         if not request.POST.get("Health Practitioner", None) == None:
    #             referred_by.health_practitioner = True
    #         if not request.POST.get("Alcoholics Anonymous", None) == None:
    #             referred_by.alcoholics_anonymous = True
    #         if not request.POST.get("Drug Treatment Group", None) == None:
    #             referred_by.drug_treatment_group = True
    #         if not request.POST.get("Advertisement", None) == None:
    #             referred_by.advertisement = True
    #         if not request.POST.get("OtherCheckbox", None) == None:
    #             print("made it to step 1")
    #             referred_by.other2 = request.POST.get('other2', False)
    #             print(referred_by.other2)
    #             if request.POST.get("other2", False) != False:
    #                 print("made it to step 2")

    #         request.session['temp_data'] = client.client_number

    #         #save client as the primary key of services_required and referred_by
    #         services_required.client1 = client
    #         referred_by.client1 = client

    #         #save the forms
    #         client.services_required = services_required
    #         services_required.save()
    #         referred_by.save()
    #         toSave = client
    #         toSave.save()
    #         print(request.session['temp_data'])
    #         return redirect(request.META['HTTP_REFERER'], request.session['temp_data'])

    #     else:
    #         print(form.errors)
    #         print(form2.errors)
    #         print(form3.errors)
    # else:
    #     if 'temp_data' in request.session:
    #         data['previous_success'] = True
    #         data['c_num'] = request.session['temp_data']
    #     form = PatientIntakeForm()
    # data['form'] = form

    if request.method == "POST":
        form = patientForm(request.POST)
        if form.is_valid():
            create_models(form)
    else:
        if 'temp_data' in request.session:
            data['previous_success'] = True
            data['c_num'] = request.session['temp_data']
        data['form'] = patientForm()

    return render(request, 'stats/form.html', data)



@login_required
def profile(request):
    # Send list of keys to front end if the request came from the admin
    if request.user.is_superuser:
        keys = InviteKey.objects.all()
        data = {'keys':keys}
        return render(request, 'stats/profile.html', data)

    # Return regular page if not an admin request
    return render(request, 'stats/profile.html', {})

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



# Use Django's built in login system but redirect to the homepage if already
# logged in
def user_login(request, **kwargs):
    if request.user.is_authenticated():
        return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        return view_login(request, **kwargs)
