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
def addStudent(request):
    if request.user.item_type != User.Types.STAFF:
        messages.error(request, 'دسترسی ندارید!')
        return redirect('system:logout')

    if request.method == "POST" :
        form  = UserForm(request.POST)
        if form.is_valid():
            instance           = form.save(commit=False)
            instance.item_type = User.Types.STUDENT
            instance.save()
            sf         = StudentFields()
            sf.student = instance
            o_id       = request.POST.get('orientation')
            is_daily   = request.POST.get('is_daily')
            try:
                orientation = Orientation.objects.get(id=o_id)
            except ObjectDoesNotExist:
                messages.error(request, 'دانشجو با موفقیت اضافه نشد')        
                return redirect('staff:dashboard', username=request.user.username)
            sf.group       = orientation.group
            sf.is_daily    = True if is_daily else False
            sf.orientation = orientation
            sf.save()
            message = """دانشجو گرامی {first_name} {last_name} حساب کاربری شما در سامانه تحصیلات تکمیلی دانشگاه بوعلی سینا ایجاد شد. \n
                        برای ورود به آدرس زیر مراجعه کنید.
                        http://localhost:8000/
                        نام کاربری: {username} \n
                        گذرواژه: {password}""".format(first_name=instance.first_name, 
                                                    last_name=instance.last_name, 
                                                    username=instance.username, 
                                                    password=instance.n_code)

            send_mail(SUBJECT, 
                    message, 
                    EMAIL_HOST_USER, 
                    [instance.email], 
                    fail_silently=False)
            messages.success(request, 'دانشجو با موفقیت اضافه شد')        
            return redirect('staff:dashboard', username=request.user.username)
    else:
        form  = UserForm()

    orientations = Orientation.objects.all()
    context = {
        'form': form,
        'orientations': orientations,
    }

    return render(
            request, 
            'staff/addStudent.html', 
            context=context,
        )




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
    
    return render(request, 'staff/addGroup.html', {'form': form})


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
        return redirect('professor:dashboard', username=request.user.username)

    if request.method == "POST":
        p_id = request.POST['professor']

        try:
            professor = Professor.objects.get(id=p_id)
        except ObjectDoesNotExist:
            messages.error(request, 'استاد مورد نظر در این گروه وجود ندارد')
            return redirect('professor:set_group_admin', id=id)
        Adminstrator(group=group, professor=professor).save()
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
        
    return render(request, 'staff/setGroupAdmin.html', context=context)        
    

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
    return render(request, 'staff/addOrientation.html', context=context)


@login_required
def deleteGroup(request, id):
    return render(request, 'staff/error.html', context=None)


@login_required
def editGroup(request, id):
    return render(request, 'staff/error.html', context=None)


@login_required
def professorList(request, id):
    return render(request, 'staff/error.html', context=None)

@login_required
def studentList(request, id):
    return render(request, 'staff/error.html', context=None)


# @login_required
# def error(request):
#     return render(request, 'staff/error.html', context=None)


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
    return render(request, 'staff/groups.html', context={'groups': groups})

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
    return render(request, 'staff/groups.html', context={'groups': groups})
