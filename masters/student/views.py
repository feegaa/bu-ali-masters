from django.shortcuts import render, redirect
from jalali_date import datetime2jalali, date2jalali
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

import jdatetime

from student.forms import DissertationForm, DRForm
from student.models import Dissertation
from system.models import User



# Create your views here.
def juryRequest(request):
    return render(request, 'student/juryRequest.html', {})
def achievementReport(request):
    return render(request, 'student/achievementReport.html', {})
def achievementReportEdit(request):
    return render(request, 'student/achievementReportEdit.html', {})
def dissertationReportEdit(request):
    return render(request, 'student/dissertationReportEdit.html', {})
def dashboard(request, username):
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
    if request.user.item_type == User.Types.STUDENT:
        pass
    else:
        return redirect('system:logout')
    try:
        Dissertation.objects.get(student=request.user)
        return redirect('student:disserta')
    except ObjectDoesNotExist:
        pass
    if request.method == "POST":
        form = DissertationForm(request.POST)
        print(form)
        if form.is_valid():
            instance = form.save(commit=False)
            jdate = request.POST['jury_date'].split('-')
            instance.student = request.user
            instance.jury_date = jdatetime.date(int(jdate[0]), int(jdate[1]), int(jdate[2]))
            instance.save()
            return redirect('student:dashboard', username=request.user.username)
            # jalali_join = date2jalali(the_date).strftime('%y/%m/%d')
    else:
        form = DissertationForm()
    context = {
        'form': form
    }
    return render(request, 'student/dissertationCreate.html', context=context)


@login_required
def dissertationReport(request):
    # jalali_join = datetime2jalali(request.user.date_joined).strftime('%y/%m/%d _ %H:%M:%S')
    if request.user.item_type == User.Types.STUDENT:
        pass
    else:
        return redirect('system:logout')
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
            instance.jury_date = jdatetime.date(int(jdate[0]), int(jdate[1]), int(jdate[2]))
            instance.save()
            return redirect('student:dashboard', username=request.user.username)
            # jalali_join = date2jalali(the_date).strftime('%y/%m/%d')
    else:
        form = DissertationForm()
    context = {
        'form': form
    }
    return render(request, 'student/dissertationCreate.html', context=context)
