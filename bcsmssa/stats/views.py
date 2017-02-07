from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def homepage(request):
    return render(request, 'stats/homepage.html', {})

@login_required
def form(request):
    return render(request, 'stats/form.html', {})
