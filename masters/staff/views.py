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
def addGroup(request):
    if request.user.item_type != User.Types.STAFF:
        messages.error(request, 'دسترسی ندارید!')
        return redirect('system:logout')

    if request.method == "POST":
        form = GroupForm(request.POST)        
        if form.is_valid():
            instance = form.save(commit=False)
            user     = request.user 
            college  = ''
            if user.item_type == User.Types.STAFF:
                college = user.stafffields.college
            else:
                return redirect('system:logout')
            instance.college = college
            instance.save()
            messages.success(request, 'گروه اضافه شد')        
            return redirect('staff:dashboard', username=user.username)
    else:
        form = GroupForm()
    
    return render(request, 'staff/system/addGroup.html', {'form': form})



@login_required
def editGroup(request, id):

    return render(request, 'staff/error.html', context=None)



@login_required
def editOrientation(request, id):

    return render(request, 'staff/error.html', context=None)


@login_required
def deleteOrientation(request, id):

    return render(request, 'staff/error.html', context=None)



@login_required
def setGroupAdmin(request, id):
    if request.user.item_type != User.Types.STAFF:
        messages.error(request, 'Access denied!')
        return redirect('system:logout')
    try:
        group = Group.objects.get(id=id)
        pfs   = ProfessorFields.objects.filter(group=group)
    except ObjectDoesNotExist:
        messages.error(request, 'گروه مورد نظر وجود ندارد')
        return redirect('staff:dashboard', username=request.user.username)

    if request.method == "POST":
        p_id = request.POST['professor']

        try:
            professor = Professor.objects.get(id=p_id)
        except ObjectDoesNotExist:
            messages.error(request, 'استاد مورد نظر در این گروه وجود ندارد')
            return redirect('professor:set_group_admin', id=id)
        Adminstrator(group=group, professor=professor).save()
        professor.professorfields.is_adminstrator = True
        group.has_admin                           = True
        professor.professorfields.save()
        group.save()
        messages.success(request, 'دکتر {first_name} {last_name} به عنوان مدیر گروه {title} انتخاب شدند.'.format(first_name=professor.first_name,
                                                                                                                last_name=professor.last_name,
                                                                                                                title=group.title))
        message = """استاد گرامی {first_name} {last_name} شما به عنوان مدیر گروه {title} تعیین شدید. \n
                    """.format(first_name=professor.first_name, 
                                last_name=professor.last_name,
                                title=group.title,) 

        send_mail(SUBJECT, 
                message, 
                EMAIL_HOST_USER, 
                [professor.email], 
                fail_silently=False)                                                                                            
        return redirect('staff:dashboard', username=request.user.username)
    context = {
        'group': group,
        'pfs': pfs
    }
        
    return render(request, 'staff/system/setGroupAdmin.html', context=context)        
    

@login_required
def addOrientation(request):

    user     = request.user 
    
    if user.item_type == User.Types.STAFF:
        college = user.stafffields.college
    else:
        return redirect('system:logout')

    if request.method == "POST":
        o_form = OrientationForm(request.POST)        

        if o_form.is_valid():
            group_id = request.POST.get('group')
            try:
                group = Group.objects.get(id=group_id)
            except ObjectDoesNotExist:
                return redirect('staff:dashboard', username=user.username)

            instance       = o_form.save(commit=False)
            instance.group = group
            instance.save()
            messages.success(request, 'گرایش اضافه شد')        
            return redirect('staff:dashboard', username=user.username)
    
    else:
        o_form  = OrientationForm()

    groups  = Group.objects.filter(college=college)
    context = {
        'o_form': o_form,
        'groups': groups
    }
    return render(request, 'staff/system/addOrientation.html', context=context)

@login_required
def groupOrientationList(request, id):
    if request.user.item_type != User.Types.STAFF:
        return redirect('system:logout')
    try:
        group = Group.objects.get(id=id)
    except:
        messages.error(request, 'گروه پیدا نشد!')
        return redirect('staff:dashboard', username=request.user.username)
    ors = Orientation.objects.filter(group=id)
    context = {
        'ors': ors,
        'group': group,
    }
    return render(request, 'staff/system/ors.html', context=context)


@login_required
def error(request):
    return render(request, 'staff/error.html', context=None)

@login_required
def groups(request):
    if request.user.item_type != User.Types.STAFF:
        messages.error(request, 'دسترسی ندارید!')
        return redirect('system:logout')
    else:
        pass

    try:
        clg    = request.user.stafffields.college
        groups = Group.objects.get(college=clg)
    except:
        return redirect('system:logout')
    return render(request, 'staff/system/groups.html', context={'groups': groups})

@login_required
def dashboard(request, username):
    if request.user.item_type != User.Types.STAFF:
        messages.error(request, 'دسترسی ندارید!')
        return redirect('system:logout')
    else:
        pass

    try:
        clg    = request.user.stafffields.college
        groups = Group.objects.filter(college=clg)
    except:
        return redirect('system:logout')
    return render(request, 'staff/dashboard.html', context={'groups': groups})




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
