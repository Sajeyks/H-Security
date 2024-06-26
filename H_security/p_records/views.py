from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import HospitalVisit, HealthRecord
from .forms import UpdatePreconditionsForm, HospitalVisitForm
from django.db.models import Q

# Create your views here.

@login_required
@user_passes_test(lambda user: not user.groups.filter(name='Non-Staff Group').exists())
def healthRecord(request):
    records = HealthRecord.for_group(request.user)
    
    page = request.GET.get('page', 1)
    paginator = Paginator(records, 50)
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

@login_required
@user_passes_test(lambda user: not user.groups.filter(name='Non-Staff Group').exists())
def recordDetails(request, pk):
    recorddetails = HealthRecord.details_for_group(request.user, pk)

    preconditions_form = UpdatePreconditionsForm(instance=recorddetails)

    if request.method == 'POST':
        preconditions_form = UpdatePreconditionsForm(request.POST, instance=recorddetails)

        if preconditions_form.is_valid():
            preconditions_form.save()
            messages.success(request, 'Pre-conditions updated successfully!')
        else:
            print(preconditions_form.errors)

    context = {
        "Recorddetails": recorddetails,
        "preconditions_form": preconditions_form,
    }

    return render(request, "p_records/record-details.html", context)

@login_required
@user_passes_test(lambda user: not user.groups.filter(name='Non-Staff Group').exists())
def searchRecords(request):
    query = request.GET.get('search')
    if query:
        records = HealthRecord.objects.filter(
        Q(owner__national_id_no__icontains=query ) | 
        Q(owner__name__icontains=query) |
        Q(owner__email__icontains=query)
        )
        print(query)
        page = request.GET.get('page', 1)
        paginator = Paginator(records, 15)
        try:
            records = paginator.page(page)
        except PageNotAnInteger:
            records = paginator.page(1)
        except EmptyPage:
            records = paginator.page(paginator.num_pages)


        context = {
            'Records': records,
            'query': query
        }
        return render(request, "p_records/record-search.html", context)
    
		
    else:
        records = HealthRecord.objects.all()

        page = request.GET.get('page', 1)
        paginator = Paginator(records, 15)
        try:
            records = paginator.page(page)
        except PageNotAnInteger:
            records = paginator.page(1)
        except EmptyPage:
            records = paginator.page(paginator.num_pages)
            
        context = {
            'Records': records,
        }

        return render(request, "p_records/healthrecords.html", context)

@login_required
@user_passes_test(lambda user: not user.groups.filter(name='Non-Staff Group').exists())
def addHospitalVisit(request, pk):
    recorddetails = HealthRecord.objects.get(pk=pk)
    editor = request.user

    if request.method == 'POST':
        visit_form = HospitalVisitForm(request.POST)

        if visit_form.is_valid():
            new_instance = visit_form.save(commit=False)
            new_instance.save()
            new_instance.edited_by.add(editor)
            new_instance.save()
            recorddetails.hospital_visits.add(new_instance)
            messages.success(request, 'Hospital visit added successfully!')
            return redirect('records-details', pk=pk)
        else:
            print(visit_form.errors)
    else:
        visit_form = HospitalVisitForm()

    context = {
        "Recorddetails": recorddetails,
        "visit_form": visit_form,
    }

    return render(request, "p_records/add-hospital-visit.html", context)


@login_required
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

@login_required
@user_passes_test(lambda user: not user.groups.filter(name='Non-Staff Group').exists())
def deleteHospitalVisit(request, pk):
    visit = HospitalVisit.objects.get(pk=pk)
    healthRecord = HealthRecord.objects.get(hospital_visits=visit)
    return_id = healthRecord.pk
    visit.delete()
    messages.success(request, 'Hospital visit deleted successfully!')
    return redirect('records-details', pk=return_id)
    


def otpVerify(request,uid):
        pass    