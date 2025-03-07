from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseServerError, HttpResponse


from generalproductinfo.models import GeneralProductInformation

# Create your views here.
def dashboard(request, pk=None, code=None):
    if pk is None and code is None:
        raise Exception("No primary key or code provided")
    
    if pk is not None:
        product = get_object_or_404(GeneralProductInformation, pk=pk)
    else:
        product = get_object_or_404(GeneralProductInformation, battery_id=code)
        
    print('data : ', product.material_composition.battery_materials.all())
    
    context = {
        'product': product
    }
    
    return render(request, 'dashboard.html', context)