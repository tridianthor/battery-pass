from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from utils.resp import Resp
from utils.upload_util import Upload
from utils.validators import validate_json

from .models import Labeling, LabelingEntity, LabelingSubject
from .forms import LabelingInsertForm, LabelingUpdateForm, LabelingEntityInsertForm, LabelingEntityUpdateForm
from .const import declaration_path, result_of_test_path, labeling_symbol_path

from dal import autocomplete

from datetime import datetime

import traceback
import json
import traceback

paths = {
    "declaration_path": declaration_path,
    "result_of_test_path": result_of_test_path
}

class LabelingEntityAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = LabelingEntity.objects.all()
        
        if self.q:
            qs = qs.filter(labeling_subject__istartswith=self.q)
            print(qs)
        return qs

# Create your views here.
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

def delete_labeling(request, pk):
    if(pk):
        labeling = get_object_or_404(Labeling, pk=pk)
        Upload.remove_files([f'{declaration_path}/{labeling.declaration_of_conformity}',f'{result_of_test_path}/{labeling.result_of_test_report}'])
        labeling.delete()
        return redirect('/labeling')
    
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

def update_labeling(request, pk):
    labeling = get_object_or_404(Labeling, pk=pk)
    form = LabelingUpdateForm(request.POST or None, request.FILES or None, instance=labeling)
    form_type = 'update'
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

def delete_labeling_entity(request, pk):
    if(pk):
        labeling_entity = get_object_or_404(LabelingEntity, pk=pk)
        print(f"{labeling_symbol_path}/{labeling_entity.labeling_symbol}")
        Upload.remove_files([f"{labeling_symbol_path}/{labeling_entity.labeling_symbol}"])
        labeling_entity.delete()
        return redirect('/labeling/entity')

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