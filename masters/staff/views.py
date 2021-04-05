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
from system.models import Group, User, Orientation
from professor.models import ProfessorFields
from student.models import Student, StudentFields


@login_required
def addStudent(request):
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
            print('successfully added')
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


def addGroup(request):
    if request.method == "POST":
        group_form = GroupForm(request.POST)        
        if group_form.is_valid():
            instance = group_form.save(commit=False)
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
        group_form = GroupForm()
    
    return render(request, 'staff/addGroup.html', {'group_form': group_form})


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


def error(request):
    return render(request, 'staff/error.html', context=None)

def groups(request):
    try:
        clg    = request.user.stafffields.college
        groups = Group.objects.get(college=clg)
    except:
        return redirect('system:logout')
    return render(request, 'staff/groups.html', context={'groups': groups})


def dashboard(request, username):
    return render(request, 'staff/dashboard.html', context=None)

