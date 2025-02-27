from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.contrib.auth.decorators import login_required, permission_required

from components.form.FilterForm import DateFilterForm
from utils.resp import Resp
from utils.upload_util import Upload

from .models import Labeling, LabelingEntity
from .forms import LabelingInsertForm, LabelingUpdateForm, LabelingEntityInsertForm, LabelingEntityUpdateForm
from .const import declaration_path, result_of_test_path, labeling_symbol_path

import plotly.express as px

from dal import autocomplete

from datetime import datetime

import traceback
import json

paths = {
    "declaration_path": declaration_path,
    "result_of_test_path": result_of_test_path
}
class LabelingEntityAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return LabelingEntity.objects.none()
        
        qs = LabelingEntity.objects.all()
        
        if self.q:
            qs = qs.filter(labeling_subject__istartswith=self.q)
            print(qs)
        return qs

@login_required(login_url="/accounts/login/")
@permission_required('labeling.view_labeling')
def labeling(request):
    labeling = Labeling.objects.filter().order_by('-id')

    per_page = 10
    paginator = Paginator(labeling, per_page)
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
        return render(request, 'labeling.html', {'exception': exception})
    return render(request, 'labeling.html', {'data': data, 'paginator': paginator, 'paths' : paths})

@login_required(login_url="/accounts/login/")
def delete_labeling(request, pk):
    if(pk):
        labeling = get_object_or_404(Labeling, pk=pk)
        Upload.remove_files([f'{declaration_path}/{labeling.declaration_of_conformity}',f'{result_of_test_path}/{labeling.result_of_test_report}'])
        labeling.delete()
        return redirect('/labeling')

@login_required(login_url="/accounts/login/")
def insert_labeling(request):
    form = LabelingInsertForm(request.POST or None, request.FILES or None)
    form_type = 'insert'
    if request.method == 'POST':
        if form.is_valid():
            try:
                declaration_of_conformity = request.FILES['declaration_of_conformity']
                result_of_test_report = request.FILES['result_of_test_report']
                
                declaration_of_conformity_filename = Upload.handle_single_upload(declaration_path, declaration_of_conformity, f'declaration_of_conformity_{datetime.now().timestamp()}')
                result_of_test_report_filename = Upload.handle_single_upload(result_of_test_path, result_of_test_report, f'result_of_test_report_{datetime.now().timestamp()}')
                
                labeling = Labeling(
                    declaration_of_conformity=declaration_of_conformity_filename,
                    result_of_test_report=result_of_test_report_filename,
                )
                
                labeling.save()
                print(form.cleaned_data['labels'])
                labeling.labels.set(form.cleaned_data['labels'])
                return redirect('/labeling')
            except Exception as exception:
                tb = traceback.format_exc()
                print(f"errors : {exception}\ntrace : {tb}")
                return render(request, 'labeling_form.html', {'form': form, 'form_type':form_type, "message":"Upload failed"})
    return render(request, 'labeling_form.html', {'form': form, 'form_type':form_type})    

@login_required(login_url="/accounts/login/")
def update_labeling(request, pk):
    labeling = get_object_or_404(Labeling, pk=pk)
    form = LabelingUpdateForm(request.POST or None, request.FILES or None, instance=labeling)
    form_type = 'update'
    print(paths)
    if request.method == 'POST':
        if form.is_valid():
            try:
                if request.FILES.keys() >= {"declaration_of_conformity"}:
                    declaration_of_conformity = request.FILES['declaration_of_conformity']
                    declaration_of_conformity_filename = Upload.handle_single_upload(declaration_path, declaration_of_conformity, f'declaration_of_conformity_{datetime.now().timestamp()}')
                    Upload.remove_files([f"{declaration_path}/{labeling.declaration_of_conformity}"])
                else:
                    declaration_of_conformity_filename = None
                    
                if request.FILES.keys() >= {"result_of_test_report"}:
                    result_of_test_report = request.FILES['result_of_test_report']
                    result_of_test_report_filename = Upload.handle_single_upload(result_of_test_path, result_of_test_report, f'result_of_test_report_{datetime.now().timestamp()}')
                    Upload.remove_files([f"{result_of_test_path}/{labeling.result_of_test_report}"])
                else:
                    result_of_test_report_filename = None
                
                if declaration_of_conformity_filename is not None:
                    labeling.declaration_of_conformity = declaration_of_conformity_filename
                if result_of_test_report_filename is not None:
                    labeling.result_of_test_report = result_of_test_report_filename
                
                labeling.save()
                
                labeling.labels.set(form.cleaned_data['labels'])
                
                return redirect('/labeling')
            except Exception as exception:
                tb = traceback.format_exc()
                print(f"errors : {exception}\ntrace : {tb}")
                return render(request, 'labeling_form.html', {'form': form, 'form_type': form_type, "paths":paths, "message":"Upload failed"})
    return render(request, 'labeling_form.html', {'form': form, 'form_type': form_type, "paths":paths})    

@login_required(login_url="/accounts/login/")
@permission_required('labeling_entity.view_labelingentity', raise_exception=True)
def labeling_entity(request):
    labeling_entity = LabelingEntity.objects.filter().order_by('-id')
    
    per_page = 10
    paginator = Paginator(labeling_entity, per_page)
    page_number = request.GET.get('page')
    
    paths = {
        "labeling_symbol_path": labeling_symbol_path
    }
    
    try:
        data = paginator.page(page_number)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(1)
    except Exception as exception:
        tb = traceback.format_exc()
        print(f"errors : {exception}\ntrace : {tb}")
        return render(request, 'labeling_entity.html', {'exception': exception})
    return render(request, 'labeling_entity.html', {'data': data, 'paginator': paginator, 'paths': paths})

@login_required(login_url="/accounts/login/")
def delete_labeling_entity(request, pk):
    if(pk):
        labeling_entity = get_object_or_404(LabelingEntity, pk=pk)
        print(f"{labeling_symbol_path}/{labeling_entity.labeling_symbol}")
        Upload.remove_files([f"{labeling_symbol_path}/{labeling_entity.labeling_symbol}"])
        labeling_entity.delete()
        return redirect('/labeling/entity')

@login_required(login_url="/accounts/login/")
def insert_labeling_entity(request):
    form = LabelingEntityInsertForm(request.POST or None, request.FILES or None)
    form_type = 'insert'
    if request.method == 'POST':
        if form.is_valid():
            try:
                labeling_symbol_file = request.FILES['labeling_symbol']
                
                labeling_symbol_filename = Upload.handle_single_upload(labeling_symbol_path, labeling_symbol_file, f"labeling_symbol_{datetime.now().timestamp()}")
                
                labeling_entity = LabelingEntity(labeling_symbol=labeling_symbol_filename, 
                    labeling_meaning=json.loads(request.POST['labeling_meaning']),
                    labeling_subject=request.POST['labeling_subject'])    
                
                labeling_entity.save()
                
                return redirect('/labeling/entity')
            except Exception as exception:
                tb = traceback.format_exc()
                print(f"errors : {exception}\ntrace : {tb}")
                return render(request, 'labeling_entity_form.html', {'form': form, "message":"Upload failed"})
        else:
            return render(request, 'labeling_entity_form.html', {'form': form, "message":"Upload failed"})
    return render(request, 'labeling_entity_form.html', {'form': form, 'form_type': form_type})

@login_required(login_url="/accounts/login/")
def update_labeling_entity(request, pk):
    labeling_entity = get_object_or_404(LabelingEntity, pk=pk)
    form = LabelingEntityUpdateForm(request.POST or None, request.FILES or None, instance = labeling_entity)
    form_type = 'update'
    paths = {
        "labeling_symbol_path": labeling_symbol_path
    }
    
    if request.method == 'POST':
        if form.is_valid():
            try:
                if request.FILES.keys() >= {"labeling_symbol"}:
                    labeling_symbol_file = request.FILES['labeling_symbol']
                    labeling_symbol_filename = Upload.handle_single_upload(labeling_symbol_path, labeling_symbol_file, f"labeling_symbol_{datetime.now().timestamp()}")
                else:
                    labeling_symbol_filename = None
                    
                #delete previous files when upload new files
                Upload.remove_files([labeling_entity.labeling_symbol])
                
                if labeling_symbol_filename is not None:
                    labeling_entity.labeling_symbol = labeling_symbol_filename
                labeling_entity.labeling_meaning = json.loads(request.POST['labeling_meaning'])
                labeling_entity.labeling_subject = request.POST['labeling_subject']
                
                labeling_entity.save()
                return redirect('/labeling/entity')
            except Exception as exception:
                tb = traceback.format_exc()
                print(f"errors : {exception}\ntrace : {tb}")
                return render(request, 'labeling_entity_form.html', {'form': form, "message":"Upload failed"})
        else:
            return render(request, 'labeling_entity_form.html', {'form': form, "message":"Upload failed"})
    return render(request, 'labeling_entity_form.html', {'form': form, 'form_type': form_type, 'paths': paths})

@login_required(login_url="/accounts/login/")
def report(request):
    chart_types = ['bar', 'line', 'pie', 'doughnut', 'radar', 'polarArea', 'scatter', 'bubble']
    chart_type = request.GET.get("chart_type", chart_types[0])
    
    if chart_type not in chart_types:
        chart_type = chart_types[0]
    
    date_filter_form = DateFilterForm(request.GET or None)
    
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    
    if start_date and end_date:
        data = LabelingEntity.objects.filter(insert_date__range=[start_date, end_date]).values('labeling_subject').annotate(total=Count('labeling_subject'))
    else:
        data = LabelingEntity.objects.values('labeling_subject').annotate(total=Count('labeling_subject'))
        
    labeling_subjects = list(item['labeling_subject'] for item in data)
    
    totals = list(item['total'] for item in data)
    
    context = {
        'labels':labeling_subjects,
        'data':totals,
        'date_filter_form':date_filter_form,
        'chart_type':chart_type
    }
    
    return render(request, 'labeling_entity_report.html', context)

@login_required(login_url="/accounts/login/")
def report_panel(request):
    date_filter_form = DateFilterForm(request.GET or None)
    
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    
    if start_date and end_date:
        data = LabelingEntity.objects.filter(insert_date__range=[start_date, end_date]).values('labeling_subject').annotate(total=Count('labeling_subject'))
    else:
        data = LabelingEntity.objects.values('labeling_subject').annotate(total=Count('labeling_subject'))
    
    labeling_subjects = list(item['labeling_subject'] for item in data)
    
    totals = list(item['total'] for item in data)
    
    try:
        fig = px.bar(x=labeling_subjects, y=totals, title="Labeling Entities")
        context = {
            'plot_html':fig.to_html(),
            'date_filter_form':date_filter_form,
        }
        return render(request, 'labeling_test.html', context)
    except ValueError as value_error:
        context = {
            'message':"No data",
            'date_filter_form':date_filter_form,
        }
        return render(request, 'labeling_test.html', context)
    except Exception as exception:
        context = {
            'message':"Unable to show data",
            'date_filter_form':date_filter_form,
        }
        return render(request, 'labeling_test.html', context)