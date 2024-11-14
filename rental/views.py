from django.shortcuts import render,redirect
from .models import *
from .forms import PropertyForm
# Create your views here.
def home(request):
    return render(request, template_name="home.html")



def property(request):
    property=Property.objects.all()
    context={
         'property':property,
     }
    return render(request, template_name="property.html",context=context)
def propertydetails(request,id):
     property=Property.objects.get(pk=id)
     context={
         'property':property,
     }
     return render(request,template_name="propertydetails.html",context=context)

def add_property(request):
    form = PropertyForm()
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('property')
    return render(request, template_name='add_property.html', context = {'form':form,})

def update_property(request, id):
    property=Property.objects.get(pk=id)
    form=PropertyForm(instance=property)
    if request.method =='POST':
        form = PropertyForm(request.POST, request.FILES, instance=property)
        if form.is_valid():
            form.save()
            return redirect('property')
    return render(request, template_name='add_property.html', context = {'form':form,})

def delete_property(request, id):
    Property.objects.get(pk=id).delete()
    return redirect('property')