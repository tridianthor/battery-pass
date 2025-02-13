from django.shortcuts import render

# Create your views here.

def duediligence(request):
    return render(request, 'duediligence/duediligence.html')

def duediligence_form(request):
    return render(request, 'duediligence/duediligence_forms.html')
