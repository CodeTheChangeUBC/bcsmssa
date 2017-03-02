from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from stats.models import InviteKey

@login_required
def profile(request):

    # Send list of users to front end if the request came from the admin
    if request.user.is_superuser:
        users = User.objects.all()
        return render(request, 'stats/profile.html', {'users' : users})

    # Normal request
    return render(request, 'stats/profile.html', {})

@login_required
def homepage(request):
    return render(request, 'stats/homepage.html', {})

@login_required
def form(request):
    return render(request, 'stats/form.html', {})

@login_required
def new_invite_key(request):
    # Only admin can create new invite keys
    if request.user.is_superuser:
        if request.method == 'POST':
            new_key = InviteKey.objects.create()
            data = { 'success': new_key.id }
            return JsonResponse(data)

    # Return bad request error if http request was not POST
    return HttpResponseBadRequest()
