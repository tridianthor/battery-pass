from django.shortcuts import render
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required, permission_required

from utils.form_style import split_form
from utils.upload_util import Upload
from utils.resp import Resp

from .models import CarbonFootprintPerLifecycleStageEntity, CarbonFootprintForBatteries
from .forms import CarbonFootprintsLifecycleForm, CFForBatteriesInsertForm, CFForBatteriesUpdateForm
from .const import carbon_footprint_study_path

from dal import autocomplete

import traceback
class CarbonFootprintsLifecycleAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return CarbonFootprintPerLifecycleStageEntity.objects.none()
        
        qs = CarbonFootprintPerLifecycleStageEntity.objects.all()
        
        if self.q:
            qs = qs.filter(lifecycle_stage__istartswith=self.q)
        return qs

@login_required(login_url="/accounts/login/")
@permission_required('carbonfootprints.view_carbonfootprintforbatteries')
def carbon_footprints(request):
    carbon_footprints = CarbonFootprintForBatteries.objects.filter().order_by('-id')
    
    per_page = 10
    paginator = Paginator(carbon_footprints, per_page)
    page_number = request.GET.get('page')
    
    try:
        data = paginator.page(page_number)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(1)
    except Exception as exception:
        tb = traceback.format_exc()
        print(f"errors : {exception}\ntrace : {tb}")
        return render(request, 'carbon_footprints.html', {'exception': exception})
    return render(request, 'carbon_footprints.html', {'data': data, 'paginator': paginator})

@login_required(login_url="/accounts/login/")
def delete_carbon_footprints(request, pk):
    if pk:
        carbon_footprints = get_object_or_404(CarbonFootprintForBatteries, pk=pk)
        
        Upload.remove_files([f"{carbon_footprint_study_path}/{carbon_footprints.carbon_footprint_study}"])
        
        carbon_footprints.delete()
        return redirect('/carbonfootprints')
    
@login_required(login_url="/accounts/login/")
def insert_carbon_footprints(request):
    form_type = 'insert'
    form = CFForBatteriesInsertForm()
    if request.method == 'POST':
        form = CFForBatteriesInsertForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/carbonfootprints')
        else:
            print(form.errors)
    field_rows = split_form(form)
    return render(request, 'carbon_footprints_form.html', {'form': form, 'form_type': form_type, 'field_rows': field_rows})

@login_required(login_url="/accounts/login/")
def update_carbon_footprints(request, pk):
    carbon_footprints = get_object_or_404(CarbonFootprintForBatteries, pk=pk)
    form = CFForBatteriesInsertForm(instance=carbon_footprints)
    form_type = 'update'
    if request.method == 'POST':
        form = CFForBatteriesUpdateForm(request.POST, instance=carbon_footprints)
        if form.is_valid():
            form.save()
            return redirect('/carbonfootprints')
        else:
            print(form.errors)
    field_rows = split_form(form)
    return render(request, 'carbon_footprints_form.html', {'form': form, 'form_type': form_type, 'field_rows': field_rows})

@login_required(login_url="/accounts/login/")
@permission_required('carbonfootprints.view_carbonfootprintperlifecyclestageentity')
def carbon_footprints_lifecycles(request):
    carbon_footprints_lifecycles = CarbonFootprintPerLifecycleStageEntity.objects.filter().order_by('-id')
    
    per_page = 10
    paginator = Paginator(carbon_footprints_lifecycles, per_page)
    page_number = request.GET.get('page')
    
    try:
        data = paginator.page(page_number)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(1)
    except Exception as exception:
        tb = traceback.format_exc()
        print(f"errors : {exception}\ntrace : {tb}")
        return render(request, 'carbon_footprints_lifecycles.html', {'exception': exception})
    return render(request, 'carbon_footprints_lifecycles.html', {'data': data, 'paginator': paginator})

@login_required(login_url="/accounts/login/")
def delete_carbon_footprints_lifecycle(request, pk):
    if pk:
        carbon_footprints_lifecycles = get_object_or_404(CarbonFootprintPerLifecycleStageEntity, pk=pk)
        carbon_footprints_lifecycles.delete()
        return redirect('/carbonfootprints/lifecycles/')

@login_required(login_url="/accounts/login/")
def insert_carbon_footprints_lifecycle(request):
    form_type = 'insert'
    form = CarbonFootprintsLifecycleForm()
    if request.method == 'POST':
        form = CarbonFootprintsLifecycleForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('/carbonfootprints/lifecycles/')
            except Exception as exception:
                tb = traceback.format_exc()
                print(f"errors : {exception}\ntrace : {tb}")
    field_rows = split_form(form)
    return render(request, 'carbon_footprints_lifecycles_form.html', {'form': form, 'form_type': form_type, 'field_rows': field_rows})

@login_required(login_url="/accounts/login/")
def update_carbon_footprints_lifecycle(request, pk):
    carbon_footprints_lifecycles = get_object_or_404(CarbonFootprintPerLifecycleStageEntity, pk=pk)
    form = CarbonFootprintsLifecycleForm(instance=carbon_footprints_lifecycles)
    form_type = 'update'
    if request.method == 'POST':
        form = CarbonFootprintsLifecycleForm(request.POST, instance=carbon_footprints_lifecycles)
        if form.is_valid():
            try:
                form.save()
                return redirect('/carbonfootprints/lifecycles/')
            except Exception as exception:
                tb = traceback.format_exc()
                print(f"errors : {exception}\ntrace : {tb}")
                return render(request, 'carbon_footprints_lifecycles_form.html', {'form': form, "message":"Upload failed"})
    field_rows = split_form(form)
    return render(request, 'carbon_footprints_lifecycles_form.html', {'form': form, 'form_type': form_type, 'field_rows': field_rows})

