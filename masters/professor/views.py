from django.shortcuts import render
from django.contrib.auth.decorators import login_required 

# Create your views here.
def PHDRequest(request):
    return render(request, 'professor/PHDRequest.html', {})
def masterRequest(request):
    return render(request, 'professor/masterRequest.html', {})
def superviseRequest(request):
    return render(request, 'professor/superviseRequest.html', {})
def juryInvite(request):
    return render(request, 'professor/juryInvite.html', {})

@login_required
def dashboard(request, username):
    return render(request, 'professor/dashboard.html', {})
