from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .forms import GeneralProductInfoForm
from .models import GeneralProductInformation, GeneralProductInfoFilter

from utils.const import is_summary, is_form
from utils.form import split_form, identify_related_fields

import django_tables2 as tables
from django_tables2 import RequestConfig

# Create your views here.

class GeneralProductInfoTable(tables.Table):
    detail = tables.TemplateColumn(
        template_name='table-action-template.html', 
        orderable=False,
        extra_context={
            'is_summary': is_summary,
            'is_form': True,
        }) 
    class Meta:
        model = GeneralProductInformation
        template_name = 'table-template.html'
        fields = ('battery_passport_identifier', 'battery_category', 'manufacturing_date', 'detail')
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
def products(request):
    search_query = request.session.get('search_query', '')
    table = GeneralProductInfoTable(GeneralProductInformation.objects.all())
    
    if request.method == 'GET' and 'search' in request.GET:
        filter = GeneralProductInfoFilter(request.GET, queryset=GeneralProductInformation.objects.all())
        
        search_query = request.GET.get('search', '')
        request.session['search_query'] = search_query
        
        print("filter qs: ", filter.qs)
        table = GeneralProductInfoTable(filter.qs)

    RequestConfig(request, paginate={'per_page': 10}).configure(table)
    context = {'table': table, 'search_query': search_query}
    return render(request, "products.html", context)

@login_required(login_url="/accounts/login/")
def delete_products(pk):
    general_product_infos = get_object_or_404(GeneralProductInformation, pk=pk)
    general_product_infos.delete()
    return redirect('/products')

@login_required(login_url="/accounts/login/")
def insert_product(request):
    form_type = 'insert'
    form = GeneralProductInfoForm()
    related, related_multi = identify_related_fields(form)
    if request.method == 'POST':
        form = GeneralProductInfoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/products')
        else:
            print(form.errors)
    field_rows = split_form(form)
    return render(request, 'product_form.html', {
        'form': form,
        'form_type': form_type,
        'field_rows': field_rows,
        'related': related,
        'related_multi': related_multi
    })

@login_required(login_url="/accounts/login/")
def update_product(request, pk):
    form_type = 'update'
    product = get_object_or_404(GeneralProductInformation, pk=pk)
    form = GeneralProductInfoForm(instance=product)
    related, related_multi = identify_related_fields(form)
    if request.method == "POST":
        form = GeneralProductInfoForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('/products')
        else:
            print(form.errors)
    field_rows = split_form(form)
    return render(request, 'product_form.html',{
        'form':form,
        'form_type': form_type,
        'field_rows': field_rows,
        'related': related,
        'related_multi': related_multi
    })
    