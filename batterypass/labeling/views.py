from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms import formset_factory

from utils.resp import Resp
from utils.upload_util import Upload
from utils.validators import validate_json

from .models import Labeling, LabelingEntity, LabelingSubject
from .forms import LabelingForm, LabelingEntityForm, LabelsRelationForm
from .const import declaration_path, result_of_test_path, labeling_symbol_path

from dal import autocomplete

from datetime import datetime

import traceback
import json
import traceback

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
    return render(request, 'labeling.html', {'data': data, 'paginator': paginator})

def delete_labeling(request, pk):
    if(pk):
        labeling = get_object_or_404(Labeling, pk=pk)
        
        for label in labeling.labels.all():
            label.delete()
        
        labeling.delete()
        return redirect('/labeling')
    
def labeling_form(request, pk=None):
    form = LabelingForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            try:
                declaration_of_conformity = request.FILES['declaration_of_conformity']
                result_of_test_report = request.FILES['result_of_test_report']
                
                declaration_of_conformity_filename = Upload.handle_single_upload(declaration_path, declaration_of_conformity, f'declaration_of_conformity_{datetime.now().timestamp()}')
                result_of_test_report_filename = Upload.handle_single_upload(result_of_test_path, result_of_test_report, f'result_of_test_report_{datetime.now().timestamp()}')
                
                if pk:
                    labeling = get_object_or_404(Labeling, pk=pk)
                    Upload.remove_to_replace([labeling.declaration_of_conformity, labeling.result_of_test_report])
                    
                    labeling.declaration_of_conformity = declaration_of_conformity_filename
                    labeling.result_of_test_report = result_of_test_report_filename
                else:
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
                return render(request, 'labeling_form.html', {'form': form, "message":"Upload failed"})
    return render(request, 'labeling_form.html', {'form': form})    

def labeling_entity(request):
    labeling_entity = LabelingEntity.objects.filter().order_by('-id')
    
    per_page = 10
    paginator = Paginator(labeling_entity, per_page)
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
        return render(request, 'labeling_entity.html', {'exception': exception})
    return render(request, 'labeling_entity.html', {'data': data, 'paginator': paginator})

def delete_labeling_entity(request, pk):
    if(pk):
        labeling_entity = get_object_or_404(LabelingEntity, pk=pk)
        labeling_entity.delete()
        return redirect('/labeling/entity')

def labeling_entity_form(request, pk=None):
    if request.method == 'POST':
        form = LabelingEntityForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            try:
                labeling_symbol_file = request.FILES['labeling_symbol']
                
                labeling_symbol_filename = Upload.handle_single_upload(labeling_symbol_path, labeling_symbol_file, f"labeling_symbol_{datetime.now().timestamp()}")
                
                if pk:
                    labeling_entity = get_object_or_404(LabelingEntity, pk=pk)
                    #delete previous files when upload new files
                    Upload.remove_to_replace([labeling_entity.labeling_symbol])
                    
                    labeling_entity.labeling_symbol = labeling_symbol_filename
                    labeling_entity.labeling_meaning = json.load(request.POST['labeling_meaning'])
                    labeling_entity.labeling_subject = request.POST['labeling_subject']
                else:
                    labeling_entity = LabelingEntity(labeling_symbol=labeling_symbol_filename, 
                                                     labeling_meaning=request.POST['labeling_meaning'],
                                                     labeling_subject=request.POST['labeling_subject'])
                labeling_entity.save()
                return redirect('/labeling/entity')
            except Exception as exception:
                tb = traceback.format_exc()
                print(f"errors : {exception}\ntrace : {tb}")
                return render(request, 'labeling_entity_form.html', {'form': form, "message":"Upload failed"})
        else:
            return render(request, 'labeling_entity_form.html', {'form': form, "message":"Upload failed"})
    form = LabelingEntityForm()
    form_type = 'create'
    return render(request, 'labeling_entity_form.html', {'form': form, 'form_type': form_type})