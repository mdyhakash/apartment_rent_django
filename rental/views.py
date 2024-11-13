from django.shortcuts import render
from .models import *

# Create your views here.
def home(request):
    return render(request, template_name="home.html")
def property(request):
    property=Property.objects.all()
    context={
         'property':property
     }
    return render(request, template_name="property.html",context=context)
def propertydetails(request,id):
     propertys=Property.objects.get(pk=id)
     context={
         'propertys':propertys
     }
     return render(request,template_name="propertydetails.html",context=context)

