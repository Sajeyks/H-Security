from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import LabTest, Diagnosis, Prescription, Bill, HospitalVisit, PreexistingCondition, HealthRecord
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
    return render(request, "healthrecords.html", context)

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
    
    context = {
        "Visitdetails": visitdetails,
        }
    
    return render(request, "hospital_visit_details.html", context)
