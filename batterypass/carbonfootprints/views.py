from django.shortcuts import render
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required, permission_required

from utils.form import split_form, identify_related_fields, identify_file_fields
from utils.upload_util import Upload
from utils.const import is_summary, is_form

import django_tables2 as tables
from django_tables2 import RequestConfig

from .models import CarbonFootprintPerLifecycleStageEntity, CarbonFootprintForBatteries, CarbonFootprintForBatteriesFilter, CarbonFootprintPerLifecycleStageEntityFilter
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

class CarbonFootprintTable(tables.Table):
    detail = tables.TemplateColumn(
        template_name='table-action-template.html', 
        orderable=False,
        extra_context={
            'is_summary': is_summary,
            'is_form': True,
        })
    class Meta:
        model = CarbonFootprintForBatteries
        template_name = 'table-template.html'
        fields = ('battery_id', 'battery_carbon_footprint', 'carbon_footprint_study', 'created_at', 'detail')
        attrs = {
            'class': 'table table-responsive table-borderless table-striped table-hover',
        }
    
    def __init__(self, *args, **kwargs):
        self.search_query = kwargs.pop('search_query', '')
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs
    
class CarbonFootprintLifecycleTable(tables.Table):
    detail = tables.TemplateColumn(
        template_name='table-action-template.html', 
        orderable=False,
        extra_context={
            'is_summary': is_summary,
            'is_form': True,
        })
    class Meta:
        model = CarbonFootprintPerLifecycleStageEntity
        template_name = 'table-template.html'
        fields = ('lifecycle_stage', 'carbon_footprint', 'created_at', 'detail')
        attrs = {
            'class': 'table table-responsive table-borderless table-striped table-hover',
        }
    
    def __init__(self, *args, **kwargs):
        self.search_query = kwargs.pop('search_query', '')
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs

@login_required(login_url="/accounts/login/")
@permission_required('carbonfootprints.view_carbonfootprintforbatteries')
def carbon_footprints(request):
    search_query = request.session.get('search_query', '')
    table = CarbonFootprintTable(CarbonFootprintForBatteries.objects.all())
    
    if request.method == 'GET' and 'search' in request.GET:
        filter = CarbonFootprintForBatteriesFilter(request.GET, queryset=CarbonFootprintForBatteries.objects.all())
        
        search_query = request.GET.get('search', '')
        request.session['search_query'] = search_query
        
        print("filter qs: ", filter.qs)
        table = CarbonFootprintTable(filter.qs)

    RequestConfig(request, paginate={'per_page': 10}).configure(table)
    context = {'table': table, 'search_query': search_query}
    return render(request, "carbon_footprints.html", context)

@login_required(login_url="/accounts/login/")
def delete_carbon_footprints(request, pk):
    if pk:
        carbon_footprints = get_object_or_404(CarbonFootprintForBatteries, pk=pk)
        
        Upload.remove_files([f"{carbon_footprint_study_path}/{carbon_footprints.carbon_footprint_study}"])
        
        carbon_footprints.delete()
        return redirect('/carbon_footprint')
    
@login_required(login_url="/accounts/login/")
def insert_carbon_footprints(request):
    form_type = 'insert'
    form = CFForBatteriesInsertForm()
    related, related_multi = identify_related_fields(form)
    file_fields = identify_file_fields(form)
    if request.method == 'POST':
        form = CFForBatteriesInsertForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/carbon_footprint')
        else:
            print(form.errors)
    field_rows = split_form(form)
    return render(request, 'carbon_footprints_form.html', {'form': form, 
                                                        'form_type': form_type, 
                                                        'field_rows': field_rows,
                                                        'related': related,
                                                        'related_multi': related_multi,
                                                        'file_fields': file_fields})

@login_required(login_url="/accounts/login/")
def update_carbon_footprints(request, pk):
    form_type = 'update'
    carbon_footprints = get_object_or_404(CarbonFootprintForBatteries, pk=pk)
    form = CFForBatteriesInsertForm(instance=carbon_footprints)
    related, related_multi = identify_related_fields(form)
    file_fields = identify_file_fields(form)
    if request.method == 'POST':
        form = CFForBatteriesUpdateForm(request.POST, instance=carbon_footprints)
        if form.is_valid():
            form.save()
            return redirect('/carbon_footprint')
        else:
            print(form.errors)
    field_rows = split_form(form)
    return render(request, 'carbon_footprints_form.html', {'form': form, 
                                                        'form_type': form_type, 
                                                        'field_rows': field_rows,
                                                        'related': related,
                                                        'related_multi': related_multi,
                                                        'file_fields': file_fields})

@login_required(login_url="/accounts/login/")
@permission_required('carbonfootprints.view_carbonfootprintperlifecyclestageentity')
def carbon_footprints_lifecycles(request):
    search_query = request.session.get('search_query', '')
    table = CarbonFootprintLifecycleTable(CarbonFootprintPerLifecycleStageEntity.objects.all())
    
    if request.method == 'GET' and 'search' in request.GET:
        filter = CarbonFootprintPerLifecycleStageEntityFilter(request.GET, queryset=CarbonFootprintPerLifecycleStageEntity.objects.all())
        
        search_query = request.GET.get('search', '')
        request.session['search_query'] = search_query
        
        print("filter qs: ", filter.qs)
        table = CarbonFootprintLifecycleTable(filter.qs)

    RequestConfig(request, paginate={'per_page': 10}).configure(table)
    context = {'table': table, 'search_query': search_query}
    return render(request, "carbon_footprints_lifecycles.html", context)

@login_required(login_url="/accounts/login/")
def delete_carbon_footprints_lifecycle(request, pk):
    if pk:
        carbon_footprints_lifecycles = get_object_or_404(CarbonFootprintPerLifecycleStageEntity, pk=pk)
        carbon_footprints_lifecycles.delete()
        return redirect('/carbon_footprint_per_lifecycle_stage')

@login_required(login_url="/accounts/login/")
def insert_carbon_footprints_lifecycle(request):
    form_type = 'insert'
    form = CarbonFootprintsLifecycleForm()
    if request.method == 'POST':
        form = CarbonFootprintsLifecycleForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('/carbon_footprint_per_lifecycle_stage')
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
                return redirect('/carbon_footprint_per_lifecycle_stage')
            except Exception as exception:
                tb = traceback.format_exc()
                print(f"errors : {exception}\ntrace : {tb}")
                return render(request, 'carbon_footprints_lifecycles_form.html', {'form': form, "message":"Upload failed"})
    field_rows = split_form(form)
    return render(request, 'carbon_footprints_lifecycles_form.html', {'form': form, 'form_type': form_type, 'field_rows': field_rows})

