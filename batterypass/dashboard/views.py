from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseServerError, HttpResponse
from django.views.generic import ListView


import django_tables2 as tables
from django_tables2 import SingleTableView, RequestConfig

import plotly.express as px

from generalproductinfo.models import GeneralProductInformation, GeneralProductInfoFilter

class GeneralProductInfoTable(tables.Table):
    detail = tables.TemplateColumn(template_name='battery-list-actions.html', orderable=False) 
    class Meta:
        model = GeneralProductInformation
        template_name = 'battery-table.html'
        fields = ('battery_passport_identifier', 'battery_category', 'manufacturing_date', 'detail')
        attrs = {
            'class': 'table table-borderless table-striped table-hover',
        }
    
    def __init__(self, *args, **kwargs):
        self.search_query = kwargs.pop('search_query', '')
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs

class GeneralProductInfoListView(SingleTableView):
    model = GeneralProductInformation
    table_class = GeneralProductInfoTable
    template_name = 'battery-list.html'
    
def batteries(request):
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
    return render(request, "battery-list.html", context)

def get_battery(pk=None, code=None, chart_width = None, chart_width_wide=None, chart_height = 300):
    if pk is None and code is None:
        raise Exception("No primary key or code provided")
    
    if pk is not None:
        product = get_object_or_404(GeneralProductInformation, pk=pk)
    else:
        product = get_object_or_404(GeneralProductInformation, battery_id=code)
    
    carbon_footprint_df = product.carbon_footprint.carbon_footprint_per_lifecycle_stage.all()
    recycled_content_cobalt_df = product.circularity.recycled_content.filter(recycled_material='Cobalt')
    recycled_content_lithium_df = product.circularity.recycled_content.filter(recycled_material='Lithium')
    recycled_content_nickel_df = product.circularity.recycled_content.filter(recycled_material='Nickel')
    recycled_content_lead_df = product.circularity.recycled_content.filter(recycled_material='Lead')
    
    carbon_footprint_names = list(item['lifecycle_stage'] for item in carbon_footprint_df.values())
    carbon_footprint_values = list(item['carbon_footprint'] for item in carbon_footprint_df.values())
    
    recycled_content_names = ["Pre consumer share", "Post consumer share"]
    recycled_content_cobalt_values = []
    for item in recycled_content_cobalt_df:
        recycled_content_cobalt_values.append(item.pre_consumer_share)
        recycled_content_cobalt_values.append(item.post_consumer_share)
    
    recycled_content_lithium_values = []
    for item in recycled_content_lithium_df:
        recycled_content_lithium_values.append(item.pre_consumer_share)
        recycled_content_lithium_values.append(item.post_consumer_share)
    
    recycled_content_nickel_values = []
    for item in recycled_content_nickel_df:
        recycled_content_nickel_values.append(item.pre_consumer_share)
        recycled_content_nickel_values.append(item.post_consumer_share)
    
    recycled_content_lead_values = []
    for item in recycled_content_lead_df:
        recycled_content_lead_values.append(item.pre_consumer_share)
        recycled_content_lead_values.append(item.post_consumer_share)
    
    carbon_footprint_fig = px.pie(carbon_footprint_df, values=carbon_footprint_values, names=carbon_footprint_names, title='Carbon Footprint per Lifecycle Stage', hole=0.3)
    carbon_footprint_fig.update_layout(width=chart_width_wide, height=chart_height)
    carbon_footprint_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    recycled_content_cobalt_fig = px.pie(values=recycled_content_cobalt_values, names=recycled_content_names, title='Recycled Content - Cobalt', hole=0.3)
    recycled_content_cobalt_fig.update_layout(width=chart_width, height=chart_height)
    recycled_content_cobalt_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    recycled_content_lithium_fig = px.pie(values=recycled_content_lithium_values, names=recycled_content_names, title='Recycled Content - Lithium', hole=0.3)
    recycled_content_lithium_fig.update_layout(width=chart_width, height=chart_height)
    recycled_content_lithium_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    recycled_content_nickel_fig = px.pie(values=recycled_content_nickel_values, names=recycled_content_names, title='Recycled Content - Nickel', hole=0.3)
    recycled_content_nickel_fig.update_layout(width=chart_width, height=chart_height)
    recycled_content_nickel_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    recycled_content_lead_fig = px.pie(values=recycled_content_lead_values, names=recycled_content_names, title='Recycled Content - Lead', hole=0.3)
    recycled_content_lead_fig.update_layout(width=chart_width, height=chart_height)
    recycled_content_lead_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return {
        'product': product,
        'carbon_footprint_fig': carbon_footprint_fig.to_html(),
        'recycled_content_cobalt_fig': recycled_content_cobalt_fig.to_html(),
        'recycled_content_lithium_fig': recycled_content_lithium_fig.to_html(),
        'recycled_content_nickel_fig': recycled_content_nickel_fig.to_html(),
        'recycled_content_lead_fig': recycled_content_lead_fig.to_html()
    }

def summary(request, pk=None, code=None):
    context = get_battery(pk=pk, chart_height=300)
    
    return render(request, "battery-summary.html", context)

def detail(request, pk=None, code=None):
    context = get_battery(pk, chart_width=400, chart_width_wide=350, chart_height=300)
    
    return render(request, "battery-detail.html", context)

