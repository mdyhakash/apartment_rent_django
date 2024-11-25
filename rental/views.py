from django.utils import timezone
from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from datetime import date
# Create your views here.
def home(request):
    return render(request, template_name="home.html")

#####login
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if the username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return redirect('register')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already taken.')
            return redirect('register')

        # Create user in the User model
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # Create an associated User_Profile entry
        User_Profile.objects.create(
            username=username,
            email=email,
            password=user.password,  # User password is hashed; use as-is
                  # Default user type
            join_date=date.today(),
        )

        # Authenticate and log in the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'You have successfully signed up!')
            return redirect('home')  # Redirect to a home page or dashboard

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
            return redirect('profile',user.username)
    return render(request, template_name='user/user_forms.html', context = {'form':form,})

def delete_user(request,id):
    User_Profile.objects.get(pk=id).delete()
    return redirect('user')
@login_required
def book_property(request, id):
    # Fetch the property using the provided 'id'
    property_obj = get_object_or_404(Property, id=id)

    # Retrieve the User_Profile instance for the current user
    try:
        user_profile = User_Profile.objects.get(username=request.user.username)
    except User_Profile.DoesNotExist:
        messages.error(request, "User profile not found. Please contact support.")
        return redirect('home')

    # Create the booking
    booking = Booking.objects.create(
        user=user_profile,
        property=property_obj,
        booking_date=now(),
    )
    booking.save()

    messages.success(request, "Property booked successfully!")
    return redirect('home')

def booking_success(request,id):
    book_property=Property.objects.get(pk=id)
    context={
         'book_property':book_property,
     }
    return render(request, 'book_property/booking_success.html',context=context)

@login_required
def profile(request, username):
    user_profile = get_object_or_404(User_Profile, username=username)
    return render(request, 'profile.html', {'user_profile': user_profile})