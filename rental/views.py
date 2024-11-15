from datetime import timezone
from django.shortcuts import render,redirect,HttpResponse
from .models import *
from .forms import *
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


#user

def user(request):
    user=User.objects.all()
    return render(request,template_name='user/user.html',context={'user':user,})

def add_user(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('user')
    return render(request, template_name='user/user_forms.html', context = {'form':form,})


def update_user(request,id):
    user=User.objects.get(pk=id)
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect('user')
    return render(request, template_name='user/user_forms.html', context = {'form':form,})

def delete_user(request,id):
    User.objects.get(pk=id).delete()
    return redirect('user')

def book_property(request, id):
    if request.method == 'POST':
        user = request.user
        property = Property.objects.get(pk=id)
        booking_date = timezone.now()
        date_created = timezone.now()
       
       
        booking = Booking.objects.create(
            user=user,
            property=property,
            booking_date=booking_date,
            date_created = date_created,
        )
       
        booking.save()
        property.delete()

        return redirect('booking_success')  
    else:
       
        apartment = Property.objects.get(pk=id)
        return render(request, 'booking.html', {'property': property})

def booking_success(request):
    return render(request, 'booking_success.html')