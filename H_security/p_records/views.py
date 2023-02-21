from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import HospitalVisit, HealthRecord
from .forms import UpdatePreconditionsForm, HospitalVisitForm
from django.db.models import Q

# Create your views here.

def healthRecord(request):
    records = HealthRecord.objects.all()
    
    page = request.GET.get('page', 1)
    paginator = Paginator(records, 10)
    try:
        records = paginator.page(page)
    except PageNotAnInteger:
        records = paginator.page(1)
    except EmptyPage:
        records = paginator.page(paginator.num_pages)
            
    context = {
        "Records": records,
        }
    return render(request, "p_records/healthrecords.html", context)


def recordDetails(request, pk):
    
    recorddetails = HealthRecord.objects.get(pk=pk)
    
    
    if request.method == 'POST':
        preconditions_form = UpdatePreconditionsForm(request.POST, instance=recorddetails)
        
        if preconditions_form.is_valid():
            preconditions_form.save()
            messages.success(request, 'Pre-conditions updated successfully!')
            return redirect(request.path_info)
        else:
            print(preconditions_form.errors)
    else:
        preconditions_form = UpdatePreconditionsForm(instance=recorddetails)
    
    context = {
        "Recorddetails": recorddetails,
        }
    
    return render(request, "p_records/record-details.html", context)


def hospitaVisit(request):
    visits = HospitalVisit.objects.all()
    
    page = request.GET.get('page', 1)
    paginator = Paginator(visits, 10)
    try:
        visits = paginator.page(page)
    except PageNotAnInteger:
        visits = paginator.page(1)
    except EmptyPage:
        visits = paginator.page(paginator.num_pages)
    
    context = {
        "Visits": visits,
        }
    
    return render(request, "hospital_visits.html", context)


def hospitaVisitDetails(request, pk):
    visitdetails = HospitalVisit.objects.get(pk=pk)
    health_record = HealthRecord.objects.get(hospital_visits=visitdetails)
    owner = health_record.owner
    
    if request.method == 'POST':
        visit_form = HospitalVisitForm(request.POST, instance=visitdetails)
        
        if visit_form.is_valid():
            visit_form.save()
            messages.success(request, 'Hospital visit updated successfully!')
            return redirect(request.path_info)
        else:
            print(visit_form.errors)
    else:
        visit_form = HospitalVisitForm(instance=visitdetails)
    
    context = {
        "Visitdetails": visitdetails,
        "Owner": owner,
        "form": visit_form,
        }
    
    return render(request, "p_records/hospital-visit-details.html", context)    