from django.shortcuts import render, redirect
from jalali_date import datetime2jalali, date2jalali
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
import jdatetime

from student.forms import DissertationForm, DRForm
from student.models import Dissertation
from system.models import User



# Create your views here.
def juryRequest(request):
    if request.user.item_type != User.Types.STUDENT:
        return redirect('system:logout')
    else:
        pass

    return render(request, 'student/juryRequest.html', {})
def achievementReport(request):
    if request.user.item_type != User.Types.STUDENT:
        return redirect('system:logout')
    else:
        pass

    return render(request, 'student/achievementReport.html', {})

def achievementReportEdit(request):
    if request.user.item_type != User.Types.STUDENT:
        return redirect('system:logout')
    else:
        pass

    return render(request, 'student/achievementReportEdit.html', {})

def dissertationReportEdit(request):
    if request.user.item_type != User.Types.STUDENT:
        return redirect('system:logout')
    else:
        pass

    return render(request, 'student/dissertationReportEdit.html', {})

@login_required
def dashboard(request, username):
    if request.user.item_type != User.Types.STUDENT:
        return redirect('system:logout')
    else:
        pass
    return render(request, 'student/dashboard.html', {})

@login_required
def disserta(request):
    try:
        dissertation = Dissertation.objects.get(student=request.user)
    except ObjectDoesNotExist:
        return redirect('student:dashboard', username=request.user.username)
    return render(request, 'student/disserta.html', {'disserta':dissertation})


@login_required
def dissertationCreate(request):
    # jalali_join = datetime2jalali(request.user.date_joined).strftime('%y/%m/%d _ %H:%M:%S')
    if request.user.item_type != User.Types.STUDENT:
        return redirect('system:logout')
    else:
        pass
    if request.user.studentfields.has_disserta:
        return redirect('student:dashboard')
    else:
        pass
    if request.method == "POST":
        form = DissertationForm(request.POST, request.FILES)
        print("method")
        if form.is_valid():
            print("form is valid")
            instance                  = form.save(commit=False)
            instance.student          = request.user
            request.user.studentfields.update(has_disserta=True)
            instance.save()
            messages.warning(request, '?????? ???? ???????????? ?????????????????? ?????? ???? ???????????? ????????')
            return redirect('student:dashboard', username=request.user.username)
    else:
        form = DissertationForm()
    context = {
        'form': form
    }
    return render(request, 'student/dissertationCreate.html', context=context)


@login_required
def dissertationReport(request):
    # jalali_join = datetime2jalali(request.user.date_joined).strftime('%y/%m/%d _ %H:%M:%S')
    if request.user.item_type != User.Types.STUDENT:
        return redirect('system:logout')
    else:
        pass

    try:
        Dissertation.objects.get(student=request.user)
        return redirect('student:disserta')
    except ObjectDoesNotExist:
        pass
    if request.method == "POST":
        form = DRForm(request.POST)
        if form.is_valid():
            instance         = form.save(commit=False)
            instance.student = request.user
            # instance.jury_date = jdatetime.date(int(jdate[0]), int(jdate[1]), int(jdate[2]))
            instance.save()
            return redirect('student:dashboard', username=request.user.username)
            # jalali_join = date2jalali(the_date).strftime('%y/%m/%d')
    else:
        form = DissertationForm()
    context = {
        'form': form
    }
    return render(request, 'student/dissertationCreate.html', context=context)
