from django.shortcuts import render
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

from .models import PostalAddress, ComponentEntity, SparePartSupplierEntity, SafetyMeasuresEntity, RecycledContentEntity, EndOfLifeInformationEntity, DismantlingAndRemovalDocumentation, Circularity
from .forms import PostalAddressForm, ComponentEntityForm, SparePartSupplierEntityForm

from dal import autocomplete

import traceback

#TODO add permission check

class ComponentsAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return ComponentEntity.objects.none()
        
        qs = ComponentEntity.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs

class DismantlingAndRemovalDocumentationAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return DismantlingAndRemovalDocumentation.objects.none()
        
        qs = DismantlingAndRemovalDocumentation.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs

class SparePartSupplierAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return SparePartSupplierEntity.objects.none()
        
        qs = SparePartSupplierEntity.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs

class RecycledContentAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return RecycledContentEntity.objects.none()
        
        qs = RecycledContentEntity.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs

def postal_addresses(request):
    postal_address = PostalAddress.objects.all()
    
    per_page = 10
    paginator = Paginator(postal_address, per_page)
    page_number = request.GET.get('page')
    
    try:
        data = paginator.page(page_number)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(1)
    except Exception as exc:
        tb = traceback.format_exc()
        print(f"errors : {exc}\ntrace : {tb}")
    
    return render(request, 'postal_address.html', {'data':data, 'paginator':paginator})

def delete_postal_address(request, pk):
    postal_address = get_object_or_404(PostalAddress, pk=pk)
    postal_address.delete()
    return redirect('postal_addresses')

def insert_update_postal_address(request, pk=None):
    form_type = 'insert'
    form = PostalAddressForm(request.POST or None)
    if pk:
        postal_address = get_object_or_404(PostalAddress, pk=pk)
        form_type = 'update'
        form = PostalAddressForm(request.POST or None, instance=postal_address)
    
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('/postal-addresses')
        else:
            return render(request, 'postal_address_form.html', {
                'form':form,
                'form_type':form_type
            })
    return render(request, 'postal_address_form.html', {
                'form':form,
                'form_type':form_type
            })
    
def component_entities(request):
    component_entities = ComponentEntity.objects.all()
    
    per_page = 10
    paginator = Paginator(component_entities, per_page)
    page_number = request.GET.get('page')
    
    try:
        data = paginator.page(page_number)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(1)
    except Exception as exc:
        tb = traceback.format_exc()
        print(f"errors : {exc}\ntrace : {tb}")
    
    return render(request, 'component_entities.html', {'data':data, 'paginator':paginator})

def delete_component_entity(request, pk):
    component_entity = get_object_or_404(ComponentEntity, pk=pk)
    component_entity.delete()
    return redirect('component_entities')

def insert_update_component_entity(request, pk=None):
    form_type = 'insert'
    form = ComponentEntityForm(request.POST or None)
    if pk:
        component_entity = get_object_or_404(ComponentEntity, pk=pk)
        form_type = 'update'
        form = ComponentEntityForm(request.POST or None, instance=component_entity)
    
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('/component-entities')
        else:
            return render(request, 'component_entity_form.html', {
                'form':form,
                'form_type':form_type
            })
    return render(request, 'component_entity_form.html', {
                'form':form,
                'form_type':form_type
            })
    
def spare_part_supplier_entities(request):
    spare_part_supplier_entities = SparePartSupplierEntity.objects.all()
    
    per_page = 10
    paginator = Paginator(spare_part_supplier_entities, per_page)
    page_number = request.GET.get('page')
    
    try:
        data = paginator.page(page_number)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(1)
    except Exception as exc:
        tb = traceback.format_exc()
        print(f"errors : {exc}\ntrace : {tb}")
    
    return render(request, 'spare_part_supplier_entities.html', {'data':data, 'paginator':paginator})

def delete_spare_part_supplier_entity(request, pk):
    spare_part_supplier_entity = get_object_or_404(SparePartSupplierEntity, pk=pk)
    spare_part_supplier_entity.delete()
    return redirect('spare_part_supplier_entities')

def insert_update_spare_part_supplier_entity(request, pk=None):
    form_type = 'insert'
    form = SparePartSupplierEntityForm(request.POST or None)
    if pk:
        spare_part_supplier_entity = get_object_or_404(SparePartSupplierEntity, pk=pk)
        form_type = 'update'
        form = SparePartSupplierEntityForm(request.POST or None, instance=spare_part_supplier_entity)
    
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('/spare-part-supplier-entities')
        else:
            return render(request, 'spare_part_supplier_entity_form.html', {
                'form':form,
                'form_type':form_type
            })
    return render(request, 'spare_part_supplier_entity_form.html', {
                'form':form,
                'form_type':form_type
            })
    #TODO sparepart supplier entity form template is not finished yet
    #TODO implement new form layout