from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from utils.resp import Resp
from utils.upload_util import Upload
from utils.validators import validate_pdf_file

from .forms import DueDiligenceInsertForm, DueDiligenceUpdateForm
from .models import SupplyChainDueDiligence
from .const import diligence_report_path, third_party_assurances_path

from datetime import datetime

import traceback
import os


# Create your views here.

def duediligence(request):
    duediligences = SupplyChainDueDiligence.objects.filter().order_by('-id')
    
    paths = {
        "diligence_report_path": diligence_report_path,
        "third_party_assurances_path": third_party_assurances_path
    }
    
    per_page = 5
    paginator = Paginator(duediligences, per_page)
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
        return render(request, 'duediligence.html', {"exception" : exception})
    return render(request, 'duediligence.html', {"data" : data, "paginator" : paginator, "paths" : paths})

def delete(request, pk=None):
    if(pk):
        supply_chain_due_diligence = get_object_or_404(SupplyChainDueDiligence, pk=pk)
        Upload.remove_to_replace([f"{diligence_report_path}/{supply_chain_due_diligence.supply_chain_due_diligence_report}", f'{third_party_assurances_path}/{supply_chain_due_diligence.third_party_assurances}'])    
        supply_chain_due_diligence.delete()
        return redirect('/duediligence')
    
def insert_duediligence(request):
    #create
    if(request.method == 'POST'):
        form = DueDiligenceInsertForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            try:
                diligence_report_file = request.FILES['supply_chain_due_diligence_report']
                third_party_assurances_file = request.FILES['third_party_assurances']
                
                diligence_report_filename = Upload.handle_single_upload(diligence_report_path, diligence_report_file, f"diligence_report_{datetime.now().timestamp()}")
                third_party_assurances_filename = Upload.handle_single_upload(third_party_assurances_path, third_party_assurances_file, f"third_party_{datetime.now().timestamp()}")
                
                supply_chain_due_diligence = SupplyChainDueDiligence(supply_chain_due_diligence_report=diligence_report_filename,
                                                                    third_party_assurances=third_party_assurances_filename,
                                                                    supply_chain_indices=request.POST['supply_chain_indices'])
                supply_chain_due_diligence.save()                
                return redirect('/duediligence')
            except Exception as exception:
                tb = traceback.format_exc()
                print(f"errors : {exception}\ntrace : {tb}")
                return render(request, 'duediligence_form.html', {'form': form, "message":"Upload failed"})
        else:
            return render(request, 'duediligence_form.html', {'form': form, "message":"Upload failed"})
    else:
        form = DueDiligenceInsertForm()
        form_type = 'create'
        return render(request, 'duediligence_form.html', {'form': form, 'form_type': form_type})

def update_duediligence(request, pk):
    if(request.method == 'POST'):
        form = DueDiligenceUpdateForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            try:
                if request.FILES.keys() >= {"supply_chain_due_diligence_report"}:
                    diligence_report_file = request.FILES['supply_chain_due_diligence_report']
                    diligence_report_filename = Upload.handle_single_upload(diligence_report_path, diligence_report_file, f"diligence_report_{datetime.now().timestamp()}")
                else:
                    diligence_report_filename = None
                
                if request.FILES.keys() >= {"third_party_assurances"}:
                    third_party_assurances_file = request.FILES['third_party_assurances']
                    third_party_assurances_filename = Upload.handle_single_upload(third_party_assurances_path, third_party_assurances_file, f"third_party_{datetime.now().timestamp()}")
                else:
                    third_party_assurances_filename = None
                    
                supply_chain_due_diligence = get_object_or_404(SupplyChainDueDiligence, pk=pk)
                #delete previous files when upload new files
                Upload.remove_to_replace([supply_chain_due_diligence.supply_chain_due_diligence_report, supply_chain_due_diligence.third_party_assurances])    
                
                if diligence_report_filename is not None:
                    supply_chain_due_diligence.supply_chain_due_diligence_report=diligence_report_filename
                if third_party_assurances_filename is not None:
                    supply_chain_due_diligence.third_party_assurances=third_party_assurances_filename
                supply_chain_due_diligence.supply_chain_indices=request.POST['supply_chain_indices']
                supply_chain_due_diligence.save()                
                return redirect('/duediligence')
            except Exception as exception:
                tb = traceback.format_exc()
                print(f"errors : {exception}\ntrace : {tb}")
                return render(request, 'duediligence_form.html', {'form': form, "message":"Upload failed"})
        else:
            return render(request, 'duediligence_form.html', {'form': form, "message":"Upload failed"})
    else:
        #update
        paths = {
            "diligence_report_path": diligence_report_path,
            "third_party_assurances_path": third_party_assurances_path
        }
        duediligence = get_object_or_404(SupplyChainDueDiligence, pk=pk)
        form = DueDiligenceUpdateForm(request.POST or None, request.FILES or None, instance=duediligence)
        form_type = 'update'
        return render(request, 'duediligence_form.html', {'form': form, 'form_type': form_type, 'paths': paths})

def view_pdf(request, folder, filename):
    with open(f'{folder}/{filename}', 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=some_file.pdf'
        return response
    pdf.closed  