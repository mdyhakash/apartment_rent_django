from django.utils import timezone
from django.shortcuts import render,redirect,HttpResponse
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    return render(request, template_name="home.html")

#####login
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        
        user = User.objects.create_user(username=username, email=email, password=password)

      
        request.session['signup_username'] = username
        request.session['signup_email'] = email
        request.session['signup_password'] = password

        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
           
            auth_login(request, user)
            messages.success(request, 'You have successfully signed up!')
            return redirect('login')  

    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

       
        user = authenticate(request, username=username, password=password)

        if user is not None:
           
            auth_login(request, user)
            messages.success(request, 'You have successfully logged in!')
            return redirect('home') 
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    
    return render(request, 'login.html')

@login_required
def signout(request):
    django_logout(request)
    return redirect('home') 

###login finished

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
    user=User_Profile.objects.all()
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
    user=User_Profile.objects.get(pk=id)
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect('user')
    return render(request, template_name='user/user_forms.html', context = {'form':form,})

def delete_user(request,id):
    User_Profile.objects.get(pk=id).delete()
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
       
        property = Property.objects.get(pk=id)
        return render(request, template_name='book_property/booking.html', context={'property': property})

def booking_success(request):
    return render(request, 'book_property/booking_success.html')

def profile(request):
   user_profile=User_Profile.objects.all()

   return render(request,template_name='profile.html',context={'user_profile':user_profile,})

