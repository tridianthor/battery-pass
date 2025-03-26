from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.contrib.auth.decorators import login_required, permission_required

from components.form.FilterForm import DateFilterForm
from utils.upload_util import Upload
from utils.form import split_form,identify_related_fields, identify_file_fields
from utils.const import is_summary, is_form

from .models import Labeling, LabelingEntity, LabelingFilter, LabelingEntityFilter
from .forms import LabelingInsertForm, LabelingUpdateForm, LabelingEntityInsertForm, LabelingEntityUpdateForm
from .const import declaration_path, result_of_test_path, labeling_symbol_path

import plotly.express as px

from dal import autocomplete

import django_tables2 as tables
from django_tables2 import RequestConfig

paths = {
    "declaration_path": declaration_path,
    "result_of_test_path": result_of_test_path,
    "labeling_symbol_path": labeling_symbol_path
}
class LabelingEntityAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return LabelingEntity.objects.none()
        
        qs = LabelingEntity.objects.all()
        
        if self.q:
            qs = qs.filter(labeling_subject__istartswith=self.q)
        return qs

class LabelingEntityTable(tables.Table):
    detail = tables.TemplateColumn(
        template_name='table-action-template.html', 
        orderable=False,
        extra_context={
            'is_summary': is_summary,
            'is_form': True,
        }) 
    class Meta:
        model = LabelingEntity
        template_name = 'table-template.html'
        fields = ('labeling_id', 'labeling_meaning', 'labeling_subject', 'created_at', 'detail')
        attrs = {
            'class': 'table table-responsive table-borderless table-striped table-hover',
        }
    
    def __init__(self, *args, **kwargs):
        self.search_query = kwargs.pop('search_query', '')
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs
    
class LabelingTable(tables.Table):
    detail = tables.TemplateColumn(
        template_name='table-action-template.html', 
        orderable=False,
        extra_context={
            'is_summary': is_summary,
            'is_form': True,
        }) 
    class Meta:
        model = Labeling
        template_name = 'table-template.html'
        fields = ('labeling_id', 'declaration_of_conformity', 'result_of_test_report', 'created_at', 'detail')
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
@permission_required('labeling.view_labeling')
def labeling(request):
    search_query = request.session.get('search_query', '')
    table = LabelingTable(Labeling.objects.all())
    
    if request.method == 'GET' and 'search' in request.GET:
        filter = LabelingFilter(request.GET, queryset=Labeling.objects.all())
        
        search_query = request.GET.get('search', '')
        request.session['search_query'] = search_query
        
        print("filter qs: ", filter.qs)
        table = LabelingTable(filter.qs)

    RequestConfig(request, paginate={'per_page': 10}).configure(table)
    context = {'table': table, 'search_query': search_query}
    return render(request, "labeling.html", context)

@login_required(login_url="/accounts/login/")
def delete_labeling(request, pk):
    if(pk):
        labeling = get_object_or_404(Labeling, pk=pk)
        Upload.remove_files([f'{declaration_path}/{labeling.declaration_of_conformity}',f'{result_of_test_path}/{labeling.result_of_test_report}'])
        labeling.delete()
        return redirect('/labeling')

@login_required(login_url="/accounts/login/")
def insert_labeling(request):
    form_type = 'insert'
    form = LabelingInsertForm(request.POST or None, request.FILES or None)
    related, related_multi = identify_related_fields(form)
    file_fields = identify_file_fields(form)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('/label')
    field_rows = split_form(form)
    return render(request, 'labeling_form.html', {'form': form, 
                                                'form_type':form_type,
                                                'field_rows': field_rows,
                                                'related': related,
                                                'related_multi': related_multi,
                                                'file_fields': file_fields})    

@login_required(login_url="/accounts/login/")
def update_labeling(request, pk):
    form_type = 'update'
    labeling = get_object_or_404(Labeling, pk=pk)
    form = LabelingUpdateForm(request.POST or None, request.FILES or None, instance=labeling)
    related, related_multi = identify_related_fields(form)
    file_fields = identify_file_fields(form)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('/label')
    field_rows = split_form(form)
    return render(request, 'labeling_form.html', {'form': form,
                                                'form_type': form_type,
                                                'field_rows': field_rows,
                                                'related': related,
                                                'related_multi': related_multi,
                                                'file_fields': file_fields,
                                                'paths':paths})    

@login_required(login_url="/accounts/login/")
@permission_required('labeling.view_labelingentity', raise_exception=True)
def labeling_entity(request):
    search_query = request.session.get('search_query', '')
    table = LabelingEntityTable(LabelingEntity.objects.all())
    
    if request.method == 'GET' and 'search' in request.GET:
        filter = LabelingEntityFilter(request.GET, queryset=LabelingEntity.objects.all())
        
        search_query = request.GET.get('search', '')
        request.session['search_query'] = search_query
        
        print("filter qs: ", filter.qs)
        table = LabelingEntityTable(filter.qs)

    RequestConfig(request, paginate={'per_page': 10}).configure(table)
    context = {'table': table, 'search_query': search_query}
    return render(request, "products.html", context)

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
    form_type = 'insert'
    form = LabelingEntityInsertForm(request.POST or None, request.FILES or None)
    related, related_multi = identify_related_fields(form)
    file_fields = identify_file_fields(form)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('/labels')
        else:
            print("errors: ", form.errors)
    field_rows = split_form(form)
    return render(request, 'labeling_entity_form.html', {'form': form, 
                                                        'form_type': form_type,
                                                        'field_rows': field_rows,
                                                        'related': related,
                                                        'related_multi': related_multi,
                                                        'file_fields': file_fields})

@login_required(login_url="/accounts/login/")
def update_labeling_entity(request, pk):
    form_type = 'update'
    labeling_entity = get_object_or_404(LabelingEntity, pk=pk)
    form = LabelingEntityUpdateForm(request.POST or None, request.FILES or None, instance = labeling_entity)
    related, related_multi = identify_related_fields(form)
    file_fields = identify_file_fields(form)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('/labels')
    field_rows = split_form(form)
    return render(request, 'labeling_entity_form.html', {'form': form, 
                                                        'form_type': form_type, 
                                                        'field_rows': field_rows,
                                                        'related': related,
                                                        'related_multi': related_multi,
                                                        'paths': paths})

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