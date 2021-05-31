from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings
from django.views.generic import View

from system.forms import *
from system.models import User


def home(request):
    return render(request, 'error.html', {})

def whichApp(request, user):
    if user.item_type == User.Types.PROFESSOR:
        return redirect('professor:dashboard', username=user.username)
    elif user.item_type == User.Types.STUDENT:
        return redirect('student:dashboard', username=user.username)
    elif user.item_type == User.Types.STAFF:
        return redirect('staff:dashboard', username=user.username)
    else:
        return render(request, 'error.html', {})


def loginView(request):

    user = request.user
    if user.is_authenticated:
        return whichApp(request, user)
        
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, 
                            password=password)
        if user:
            login(request, user)
            request.session['id'] = user.id
            messages.success(request, 'سلام '+str(user.username)) 
            return whichApp(request, user)

        else:
            return render(request, 'error.html', {})

    return render(request, 'system/login.html', {})


@login_required
def logoutView(request):
    try:
        request.session.delete()
        logout(request)
    except KeyError:
        return redirect('system:users')
    return redirect('system:login')




# class ResetPasswordView(View):
#     form_class = ResetPasswordForm
#     template   = settings.EMAIL_RESET_PASSWORD_TEMPLATE

#     def get(self, request, *args, **kwargs):
#         email       = self.kwargs['email']
#         email_token = self.kwargs['email_token']

#         if verifyToken(email, email_token):
#             form = self.form_class()
#             return render(request, self.template, {'form': form})
#         else:
#             return redirect('user:login')

#     def post(self, request, *args, **kwargs):
#         form     = self.form_class(request.POST)
#         username = self.kwargs['username']

#         if form.is_valid():
#             try:
#                 user = UserModel.objects.get(username=username)
#                 user.set_password(form.cleaned_data) # Deactivate account till it is confirmed
#                 user.save()

#                 messages.success(request, ('لطفا برای تکمیل ثبت نام ایمیل خودتون رو تایید کنید.'))
#                 return redirect('user:login')

#             except ObjectDoesNotExist:
#                 return redirect('user:login')

#         else:
#             return render(request, self.template, {'form': form})

