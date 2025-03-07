from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseServerError, HttpResponse

import plotly.express as px

from generalproductinfo.models import GeneralProductInformation

# Create your views here.
def dashboard(request, pk=None, code=None):
    if pk is None and code is None:
        raise Exception("No primary key or code provided")
    
    if pk is not None:
        product = get_object_or_404(GeneralProductInformation, pk=pk)
    else:
        product = get_object_or_404(GeneralProductInformation, battery_id=code)
        
    
    battery_materials = product.material_composition.battery_materials.all()
    hazardous_substances = product.material_composition.hazardous_substances.all()
    
    battery_condition = product.performance.battery_condition
    battery_technical_property = product.performance.battery_technical_properties
    battery_temperature = battery_condition.temperature_information
    
    dismantling_info = product.circularity.dismantling_and_removal_information.all()
    end_of_life_info = product.circularity.end_of_life_information
    spare_part_sources = product.circularity.spare_part_sources.all()
    
    print("data : ", battery_condition.energy_throughput)
    
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
    
    carbon_footprint_fig = px.pie(carbon_footprint_df, values=carbon_footprint_values, names=carbon_footprint_names, title='Carbon Footprint per Lifecycle Stage')
    
    recycled_content_cobalt_fig = px.pie(values=recycled_content_cobalt_values, names=recycled_content_names, title='Recycled Content - Cobalt')
    recycled_content_cobalt_fig.update_layout(width=400, height=500)
    recycled_content_lithium_fig = px.pie(values=recycled_content_lithium_values, names=recycled_content_names, title='Recycled Content - Lithium')
    recycled_content_lithium_fig.update_layout(width=400, height=500)
    recycled_content_nickel_fig = px.pie(values=recycled_content_nickel_values, names=recycled_content_names, title='Recycled Content - Nickel')
    recycled_content_nickel_fig.update_layout(width=400, height=500)
    recycled_content_lead_fig = px.pie(values=recycled_content_lead_values, names=recycled_content_names, title='Recycled Content - Lead')
    recycled_content_lead_fig.update_layout(width=400, height=500)
    
    context = {
        'product': product,
        'battery_materials': battery_materials,
        'hazardous_substances': hazardous_substances,
        'battery_condition': battery_condition,
        'battery_temperature': battery_temperature,
        'battery_technical_property': battery_technical_property,
        'dismantling_info': dismantling_info,
        'end_of_life_info': end_of_life_info,
        'spare_part_sources': spare_part_sources,
        'carbon_footprint_fig': carbon_footprint_fig.to_html(),
        'recycled_content_cobalt_fig': recycled_content_cobalt_fig.to_html(),
        'recycled_content_lithium_fig': recycled_content_lithium_fig.to_html(),
        'recycled_content_nickel_fig': recycled_content_nickel_fig.to_html(),
        'recycled_content_lead_fig': recycled_content_lead_fig.to_html()
    }
    
    return render(request, 'dashboard.html', context)