from django.utils import timezone
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from datetime import date

# Home page accessible without login
def home(request):
    return render(request, template_name="home.html")

# Registration view accessible without login
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return redirect('register')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already taken.')
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        User_Profile.objects.create(
            username=username,
            email=email,
            password=user.password,
            join_date=date.today(),
        )

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'You have successfully signed up!')
            return redirect('home')

    return render(request, 'register.html')

# Login view accessible without login
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

# Logout view protected by login_required
@login_required
def signout(request):
    django_logout(request)
    return redirect('home')

# Property views

def property(request):
    property = Property.objects.all()
    context = {'property': property}
    return render(request, template_name="property.html", context=context)


def propertydetails(request, id):
    property = Property.objects.get(pk=id)
    context = {'property': property}
    return render(request, template_name="propertydetails.html", context=context)

@login_required(login_url='register')
def add_property(request):
    form = PropertyForm()
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('property')
    return render(request, template_name='add_property.html', context={'form': form})

@login_required(login_url='register')
def update_property(request, id):
    property = Property.objects.get(pk=id)
    form = PropertyForm(instance=property)
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property)
        if form.is_valid():
            form.save()
            return redirect('property')
    return render(request, template_name='add_property.html', context={'form': form})

@login_required(login_url='register')
def delete_property(request, id):
    Property.objects.get(pk=id).delete()
    return redirect('property')

# User views
@login_required
def user(request):
    user = User_Profile.objects.all()
    return render(request, template_name='user/user.html', context={'user': user})

@login_required
def add_user(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('user')
    return render(request, template_name='user/user_forms.html', context={'form': form})

@login_required
def update_user(request, id):
    user = User_Profile.objects.get(pk=id)
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', user.username)
    return render(request, template_name='user/user_forms.html', context={'form': form})

@login_required
def delete_user(request, id):
    User_Profile.objects.get(pk=id).delete()
    return redirect('user')

@login_required(login_url='register')
def book_property(request, id):
    # Get the property object
    property_obj = get_object_or_404(Property, id=id)

    try:
        # Get the User_Profile object
        user_profile = User_Profile.objects.get(username=request.user.username)
    except User_Profile.DoesNotExist:
        messages.error(request, "User profile not found. Please contact support.")
        return redirect('home')

    if request.method == 'POST':
        # Get form data
        phone = request.POST.get('phone')
        booking_date = request.POST.get('date')

        # Create the booking object
        booking = Booking.objects.create(
            user=user_profile,
            property=property_obj,
            booking_date=booking_date or now(),  # Use the provided date or current time
        )
        booking.save()

        # Redirect to a success page or home
        messages.success(request, "Property booked successfully!")
        return redirect('booking_success', id=id)

    # Render the booking form again in case of errors
    context = {
        'property': property_obj,
        'user': request.user,
    }
    return render(request, 'book_property.html', context)
@login_required(login_url='register')
def booking_success(request, id):
    book_property = Property.objects.get(pk=id)
    context = {'book_property': book_property}
    return render(request, 'book_property/booking_success.html', context=context)

@login_required
def profile(request, username):
    user_profile = get_object_or_404(User_Profile, username=username)
    return render(request, 'profile.html', {'user_profile': user_profile})
