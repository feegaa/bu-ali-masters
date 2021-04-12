from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings
# from django.views import View

from staff.forms import UserForm, GroupForm, OrientationForm
from system.models import Group, User, Orientation, Adminstrator
from professor.models import Professor, ProfessorFields
from student.models import Student, StudentFields
from masters.settings import EMAIL_HOST_USER
from django.core.mail import send_mail


SUBJECT = 'تحصیلات تکمیلی دانشگاه بوعلی سینا'




@login_required
def addProfessor(request):
    if request.user.item_type != User.Types.STAFF:
        messages.error(request, 'دسترسی ندارید!')
        return redirect('system:logout')

    if request.method == "POST" :
        p_form  = UserForm(request.POST)
        print(p_form)
        print("method post")
        if p_form.is_valid():
            print("in p form valid")
            instance           = p_form.save(commit=False)
            instance.item_type = User.Types.PROFESSOR
            instance.save()
            pf           = ProfessorFields()
            pf.professor = instance
            group_id     = request.POST.get('group')
            last_uni     = request.POST.get('last_university')
            grade        = request.POST.get('grade')
            try:
                group = Group.objects.get(id=group_id)
            except ObjectDoesNotExist:
                messages.error(request, 'استاد با موفقیت اضافه نشد')        
                return redirect('staff:dashboard', username=request.user.username)
            pf.last_university = last_uni
            pf.group           = group
            pf.grade           = grade
            pf.save()
            message = """استاد گرامی {first_name} {last_name} حساب کاربری شما در سامانه تحصیلات تکمیلی دانشگاه بوعلی سینا ایجاد شد. \n
                        برای ورود به آدرس زیر مراجعه کنید.
                        http://localhost:8000/
                        نام کاربری: {username} \n
                        گذرواژه: {password}""".format(first_name=instance.first_name, 
                                                    last_name=instance.last_name, 
                                                    username=instance.username, 
                                                    password=instance.n_code)
            # recepient = str(sub['Email'].value())
            send_mail(SUBJECT, 
                    message, 
                    EMAIL_HOST_USER, 
                    [instance.email], 
                    fail_silently = False)
            messages.success(request, 'استاد با موفقیت اضافه شد')        
            return redirect('staff:dashboard', username=request.user.username)

    else:
        p_form  = UserForm()

    groups  = Group.objects.all()
    context = {
        'p_form': p_form,
        'groups': groups,
    }

    return render(
            request, 
            'staff/addProfessor.html', 
            context=context,
        )



@login_required
def professorEdit(request, id):
    if request.user.item_type != User.Types.STAFF:
        messages.error(request, 'دسترسی ندارید!')
        return redirect('system:logout')

    if request.method == "POST" :
        p_form  = UserForm(request.POST)
        print(p_form)
        print("method post")
        if p_form.is_valid():
            print("in p form valid")
            instance           = p_form.save(commit=False)
            instance.item_type = User.Types.PROFESSOR
            instance.save()
            pf           = ProfessorFields()
            pf.professor = instance
            group_id     = request.POST.get('group')
            last_uni     = request.POST.get('last_university')
            grade        = request.POST.get('grade')
            try:
                group = Group.objects.get(id=group_id)
            except ObjectDoesNotExist:
                messages.error(request, 'استاد با موفقیت اضافه نشد')        
                return redirect('staff:dashboard', username=request.user.username)
            pf.last_university = last_uni
            pf.group           = group
            pf.grade           = grade
            pf.save()
            message = """استاد گرامی {first_name} {last_name} حساب کاربری شما در سامانه تحصیلات تکمیلی دانشگاه بوعلی سینا ایجاد شد. \n
                        برای ورود به آدرس زیر مراجعه کنید.
                        http://localhost:8000/
                        نام کاربری: {username} \n
                        گذرواژه: {password}""".format(first_name=instance.first_name, 
                                                    last_name=instance.last_name, 
                                                    username=instance.username, 
                                                    password=instance.n_code)
            # recepient = str(sub['Email'].value())
            send_mail(SUBJECT, 
                    message, 
                    EMAIL_HOST_USER, 
                    [instance.email], 
                    fail_silently = False)
            messages.success(request, 'استاد با موفقیت اضافه شد')        
            return redirect('staff:dashboard', username=request.user.username)

    else:
        p_form  = UserForm()

    groups  = Group.objects.all()
    context = {
        'p_form': p_form,
        'groups': groups,
    }

    return render(
            request, 
            'staff/addProfessor.html', 
            context=context,
        )




@login_required
def professorList(request, id):
    return render(request, 'staff/error.html', context=None)



@login_required
def error(request):
    return render(request, 'staff/error.html', context=None)



# @login_required
# def dashboard(request):

#     try:
#         user = UserModel.objects.get(id=request.user.id)
#     except ObjectDoesNotExist:
#         return HttpResponse("چنین کاربری نداریم")

#     if request.method == "POST" :
#         update_user_form   = UserUpdateForm(data=request.POST, instance=user)
#         update_avatar_form = AvatarUpdateForm(request.POST, request.FILES, instance=user.avatarmodel)

#         if update_user_form.is_valid() and update_avatar_form.is_valid():
#             update_avatar_form.save()
#             update_user_form.save()

#             messages.success(request, 'صفحه شما بروزرسانی شد.')        
#             return redirect('user:dashboard')

#     else:
#         update_user_form = UserUpdateForm(instance=user)
#         update_avatar_form = AvatarUpdateForm(instance=user.avatarmodel)

#     context = {
#         'user_form'  : update_user_form,
#         'avatar_form': update_avatar_form,   
#         'user'       : user,
#     }

#     return render(
#             request, 
#             'user/dashboard.html', 
#             context=context
#         )
