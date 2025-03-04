from django.shortcuts import render
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required, permission_required

from utils.resp import Resp
from utils.upload_util import Upload

from .models import CarbonFootprintPerLifecycleStageEntity, CarbonFootprintForBatteries
from .forms import CFPerLifecycleSEForm

from dal import autocomplete

from datetime import datetime

import traceback

class CFPerLifecycleSEAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return CarbonFootprintPerLifecycleStageEntity.objects.none()
        
        qs = CarbonFootprintPerLifecycleStageEntity.objects.all()
        
        if self.q:
            qs = qs.filter(lifecycle_stage__istartswith=self.q)
        return qs

def cf_per_lifecycle_stage_entities(request):
    cf_per_lifecycle_stage_entities = CarbonFootprintPerLifecycleStageEntity.objects.filter().order_by('-id')
    #TODO continue here