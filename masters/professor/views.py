from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 
from system.views import logoutView, loginView
from system.models import User
from django.contrib import messages
from professor.forms import MRForm
from professor.models import MasterRequest
from django.core.exceptions import ObjectDoesNotExist


# def checkUser(request):
#     if request.user.item_type != User.Types.PROFESSOR:
#         messages.error(request, 'Access denied!')
#         return redirect('system:logout')
#     else:
#         pass

# Create your views here.
# def PHDRequest(request):
#     checkUser(request)
#     return render(request, 'professor/PHDRequest.html', {})

# @login_required
# def PHDRequest(request):
#     if request.user.item_type != User.Types.PROFESSOR:
#         messages.error(request, 'Access denied!')
#         return redirect('system:logout')
#     else:
#         pass
#     if request.method == "POST":
#         form = MRForm(request.POST)
#         if form.is_valid():
#             user = request.user
            
#     return render(request, 'professor/masterRequest.html', {})


# @login_required
# def setGroupAdmin(request, id):
#     if request.user.item_type != User.Types.PROFESSOR:
#         messages.error(request, 'Access denied!')
#         return redirect('system:logout')
#     if request.method == "POST":



@login_required
def masterRequest(request):
    if request.user.item_type != User.Types.PROFESSOR:
        messages.error(request, 'Access denied!')
        return redirect('system:logout')
    else:
        pass
    if request.method == "POST":
        form = MRForm(request.POST)
        if form.is_valid():
            instance           = form.save(commit=False)
            instance.professor = request.user
            instance.group     = request.user.professorfields.group
            instance.save()
            messages.success(request, 'درخواست با موفقیت ثبت شد. درخواست باید توسط مدیر گروه تائید شود!')
            return redirect('professor:dashboard', username=request.user.username)
    else:
        form = MRForm()
    try:
        MasterRequest.objects.get(professor=request.user)
        has = True
    except ObjectDoesNotExist:
        has = False
    context = {
        'form': form,
        'has': has
    }

    return render(request, 'professor/masterRequest.html', context=context)


@login_required
def superviseRequest(request):
    if request.user.item_type != User.Types.PROFESSOR:
        messages.error(request, 'Access denied!')
        return redirect('system:logout')
    else:
        pass
    return render(request, 'professor/superviseRequest.html', {})

@login_required
def juryInvite(request):
    if request.user.item_type != User.Types.PROFESSOR:
        messages.error(request, 'Access denied!')
        return redirect('system:logout')
    else:
        pass
    return render(request, 'professor/juryInvite.html', {})

@login_required
def dashboard(request, username):
    if request.user.item_type != User.Types.PROFESSOR:
        messages.error(request, 'Access denied!')
        return redirect('system:logout')
    
    return render(request, 'professor/dashboard.html', {})
