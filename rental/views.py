from django.shortcuts import render
from .models import *

# Create your views here.
def home(request):
    return render(request, template_name="home.html")
def apartment(request):
    apartment=Property.objects.all()
    context={
         'apartment':apartment
     }
    return render(request, template_name="apartment.html",context=context)
def propertydetails(request,id):
     propertys=Property.objects.get(pk=id)
     context={
         'propertys':propertys
     }
     return render(request,template_name="propertydetails.html",context=context)

