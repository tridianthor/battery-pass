from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from utils.resp import Resp
from utils.upload_util import Upload

from .forms import DueDiligenceForm
from .models import SupplyChainDueDiligence
from .const import diligence_report_path, third_party_assurances_path

from datetime import datetime

import traceback
import os


# Create your views here.

def duediligence(request):
    duediligences = SupplyChainDueDiligence.objects.filter().order_by('-id')
    
    for duediligence in duediligences:
        duediligence.supply_chain_due_diligence_report = os.path.basename(duediligence.supply_chain_due_diligence_report)
        duediligence.third_party_assurances = os.path.basename(duediligence.third_party_assurances)
    
    per_page = 10
    paginator = Paginator(duediligences, per_page)
    page_number = request.GET.get('page')
    try:
        data = paginator.get_page(page_number)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
    except Exception as exception:
        tb = traceback.format_exc()
        print(f"errors : {exception}\ntrace : {tb}")
        return render(request, 'duediligence.html', {"exception" : exception})
    return render(request, 'duediligence.html', {"data" : data, "paginator" : paginator})

def delete(request, pk=None):
    if(pk):
        supply_chain_due_diligence = get_object_or_404(SupplyChainDueDiligence, pk=pk)
        Upload.remove_to_replace([f"{diligence_report_path}/{supply_chain_due_diligence.supply_chain_due_diligence_report}", f'{third_party_assurances_path}/{supply_chain_due_diligence.third_party_assurances}'])    
        supply_chain_due_diligence.delete()
        return redirect('/duediligence')
def duediligence_form(request, pk=None):
    #create
    if(request.method == 'POST'):
        form = DueDiligenceForm(request.POST or None, request.FILES or None)
        if(form.is_valid):
            try:
                diligence_report = request.FILES['supply_chain_due_diligence_report']
                third_party_assurances_file = request.FILES['third_party_assurances']
                    
                diligence_report_filename = Upload.handle_single_upload(diligence_report_path, diligence_report, f"diligence_report_{datetime.now().timestamp()}")
                third_party_assurances_filename = Upload.handle_single_upload(third_party_assurances_path, third_party_assurances_file, f"third_party_{datetime.now().timestamp()}")
                
                if(pk):
                    supply_chain_due_diligence = get_object_or_404(SupplyChainDueDiligence, pk=pk)
                    #delete previous files when upload new files
                    Upload.remove_to_replace([supply_chain_due_diligence.supply_chain_due_diligence_report, supply_chain_due_diligence.third_party_assurances])    
                    
                    supply_chain_due_diligence.supply_chain_due_diligence_report=diligence_report_filename
                    supply_chain_due_diligence.third_party_assurances=third_party_assurances_filename
                    supply_chain_due_diligence.supply_chain_indices=request.POST['supply_chain_indices']
                else:
                    supply_chain_due_diligence = SupplyChainDueDiligence(supply_chain_due_diligence_report=diligence_report_filename,
                                                                    third_party_assurances=third_party_assurances_filename,
                                                                    supply_chain_indices=request.POST['supply_chain_indices'])
                
                supply_chain_due_diligence.save()
                
                form = DueDiligenceForm()
                return render(request, 'duediligence_form.html', {'form': form, 'message':"Upload success"})
            except Exception as e:
                tb = traceback.format_exc()
                print(f"errors : {e}\ntrace : {tb}")
                form = DueDiligenceForm()
                return render(request, 'duediligence_form.html', {'form': form, "message":"Upload failed"})
    else:
        #edit
        if(pk is not None):
            paths = {
                "diligence_report_path": diligence_report_path,
                "third_party_assurances_path": third_party_assurances_path
            }
            duediligence = get_object_or_404(SupplyChainDueDiligence, pk=pk)
            form = DueDiligenceForm(request.POST or None, request.FILES or None, instance=duediligence)
            form_type = 'edit'
            return render(request, 'duediligence_form.html', {'form': form, 'form_type': form_type, 'paths': paths})
        else:
            form = DueDiligenceForm()
            form_type = 'create'
            return render(request, 'duediligence_form.html', {'form': form, 'form_type': form_type})

def view_pdf(request, folder, filename):
    with open(f'{folder}/{filename}', 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline;filename=some_file.pdf'
        return response
    pdf.closed  