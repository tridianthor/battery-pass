from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

from utils.upload_util import Upload
from utils.const import is_summary, is_form
from utils.form import split_form, identify_related_fields

from components.form.FilterForm import DateFilterForm

from .forms import DueDiligenceInsertForm, DueDiligenceUpdateForm
from .models import SupplyChainDueDiligence, SupplyChainDueDiligenceFilter
from .const import diligence_report_path, third_party_assurances_path

import django_tables2 as tables
from django_tables2 import RequestConfig

import traceback

path = {
    diligence_report_path,
    third_party_assurances_path,
}

class SupplyChainDueDiligenceTable(tables.Table):
    detail = tables.TemplateColumn(
        template_name='table-action-template.html', 
        orderable=False,
        extra_context={
            'is_summary': is_summary,
            'is_form': True,
        }) 
    class Meta:
        model = SupplyChainDueDiligence
        template_name = 'table-template.html'
        fields = ('supply_chain_due_diligence_report', 'third_party_assurances', 'supply_chain_indices', 'detail')
        attrs = {
            'class': 'table table-responsive table-borderless table-striped table-hover',
        }
    
    def __init__(self, *args, **kwargs):
        self.search_query = kwargs.pop('search_query', '')
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs
    

# Create your views here.
@login_required(login_url="/accounts/login/")
def duediligence(request):
    search_query = request.session.get('search_query', '')
    table = SupplyChainDueDiligenceTable(SupplyChainDueDiligence.objects.all())
    
    if request.method == 'GET' and 'search' in request.GET:
        filter = SupplyChainDueDiligenceFilter(request.GET, queryset=SupplyChainDueDiligence.objects.all())
        
        search_query = request.GET.get('search', '')
        request.session['search_query'] = search_query
        
        print("filter qs: ", filter.qs)
        table = SupplyChainDueDiligenceTable(filter.qs)

    RequestConfig(request, paginate={'per_page': 10}).configure(table)
    context = {'table': table, 'search_query': search_query}
    return render(request, "duediligence.html", context)
    
@login_required(login_url="/accounts/login/")
def delete(request, pk):
    if pk:
        supply_chain_due_diligence = get_object_or_404(SupplyChainDueDiligence, pk=pk)
        Upload.remove_files([f"{diligence_report_path}/{supply_chain_due_diligence.supply_chain_due_diligence_report}", f'{third_party_assurances_path}/{supply_chain_due_diligence.third_party_assurances}'])    
        supply_chain_due_diligence.delete()
        return redirect('/due_diligence')

@login_required(login_url="/accounts/login/")
def insert_duediligence(request):
    form_type = 'insert'
    form = DueDiligenceInsertForm(request.POST or None, request.FILES or None)

    related, related_multi = identify_related_fields(form)
    if request.method == 'POST':
        print("FILES request : ", request.FILES);
        if form.is_valid():
            form.save()
            return redirect('/due_diligence')
        else:
            print(form.errors)
    field_rows = split_form(form)
    return render(request, 'duediligence_form.html', {'form': form,
        'form_type': form_type,
        'field_rows': field_rows,
        'related': related,
        'related_multi': related_multi})

@login_required(login_url="/accounts/login/")
def update_duediligence(request, pk):
    form_type = 'update'
    duediligence = get_object_or_404(SupplyChainDueDiligence, pk=pk)
    form = DueDiligenceInsertForm(request.POST or None, request.FILES or None, instance=duediligence)

    related, related_multi = identify_related_fields(form)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('/due_diligence')
        else:
            print(form.errors)
    field_rows = split_form(form)
    return render(request, 'duediligence_form.html', {'form': form,
        'form_type': form_type,
        'field_rows': field_rows,
        'related': related,
        'related_multi': related_multi,
        'path': path})