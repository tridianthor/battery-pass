from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

from utils.resp import Resp
from utils.upload_util import Upload

from .forms import DueDiligenceForm
from .models import SupplyChainDueDiligence
from .const import diligence_report_path, third_party_assurances_path

from datetime import datetime

import uuid
import traceback


# Create your views here.

def duediligence(request):
    return render(request, 'duediligence.html')

def duediligence_form(request):    
    if(request.method == 'POST'):
        form = DueDiligenceForm(request.POST, request.FILES)
        print(request.FILES)
        if(form.is_valid):
            try:
                diligence_report = request.FILES['supply_chain_due_diligence_report']
                third_party_assurances_file = request.FILES['third_party_assurances']
                
                diligence_report_filename = Upload.handle_single_upload(diligence_report_path, diligence_report, f"diligence_report_{datetime.now().timestamp()}")
                third_party_assurances_filename = Upload.handle_single_upload(third_party_assurances_path, third_party_assurances_file, f"third_party_{datetime.now().timestamp()}")
                
                supply_chain_due_diligence = SupplyChainDueDiligence(uuid.uuid4(), 
                                                                    f'{diligence_report_path}/{diligence_report_filename}',
                                                                    f'{third_party_assurances_path}/{third_party_assurances_filename}',
                                                                    request.POST['supply_chain_indices'])
                
                supply_chain_due_diligence.save()
                
                form = DueDiligenceForm()
                return render(request, 'duediligence_form.html', {'form': form, 'message':"Upload success"})
            except Exception as e:
                tb = traceback.format_exc()
                print(f"errors : {e}\ntrace : {tb}")
                form = DueDiligenceForm()
                return render(request, 'duediligence_form.html', {'form': form, "message":"Upload failed"})
            
    else:
        form = DueDiligenceForm()
        return render(request, 'duediligence_form.html', {'form': form})