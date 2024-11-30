from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from datetime import date


def home(request):
    user_profile =User_Profile.objects.all()
    return render(request, 'home.html', {'user_profile': user_profile})
    


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')  

        
        allowed_landlord_usernames = ['hasib_174', 'maisha_160', 'akash_153', 'saima_173']

       
        if user_type == 'landlord' and username not in allowed_landlord_usernames:
            messages.error(request, 'Only specific users can register as a landlord.')
            return redirect('register')

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
            user_type=user_type
        )

        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'You have successfully signed up!')
            return redirect('register')

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



def property(request):
    sort_by = request.GET.get('sort_by', 'location')  
    order = request.GET.get('order', 'asc')  

    
    if order == 'desc':
        sort_by = f"-{sort_by}"

    property = Property.objects.all().order_by(sort_by)
    is_landlord = check_if_landlord(request.user)

    context = {
        'property': property,
        'sort_by': sort_by.lstrip('-'),
        'order': order,
        'is_landlord': is_landlord,
    }
    return render(request, 'property.html', context)

def propertydetails(request, id):
    property = Property.objects.get(pk=id)
    context = {'property': property}
    
    return render(request, template_name="propertydetails.html", context=context)


def check_if_landlord(user):
    try:
        user_profile = User_Profile.objects.get(username=user.username)
        return user_profile.user_type == 'landlord'
    except User_Profile.DoesNotExist:
        return False

@login_required(login_url='register')
def add_property(request):
    
    if not check_if_landlord(request.user):
        messages.error(request, 'Only landlords can add properties.')
        return redirect('property')
    
    form = PropertyForm()
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('property')
    return render(request, template_name='add_property.html', context={'form': form})

def not_available(request):
    return render(request, template_name='not_available.html')
@login_required(login_url='register')
def update_property(request, id):
    
    if not check_if_landlord(request.user):
        messages.error(request, 'Only landlords can update properties.')
        return redirect('not_available')
    
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
    
    if not check_if_landlord(request.user):
        messages.error(request, 'Only landlords can delete properties.')
        return redirect('not_available')
    
    Property.objects.get(pk=id).delete()
    return redirect('property')


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
      if  check_if_landlord(request.user):
        messages.error(request, 'Only user can book properties.')
        return redirect('property')
  
      property = get_object_or_404(Property, id=id)
      user_profile = User_Profile.objects.get(username=request.user.username)
    
      booking_date = request.POST.get('date')
      booking = Booking.objects.create(
            user=user_profile,
            property=property,
            booking_date=booking_date or now(),  
        )
      booking.save()
      context={'property':property}
      return render(request, 'book_property/booking.html',context=context)

@login_required(login_url='register')
def booking_success(request, id):
    book_property = Property.objects.get(pk=id)
    context = {'book_property': book_property}
    return render(request, 'book_property/booking_success.html', context=context)

@login_required(login_url='register')
def booking_history(request):
   
    if not check_if_landlord(request.user):
        messages.error(request, 'Only landlords can view the booking history.')
        return redirect('home')

    booking = Booking.objects.all()
    context = {'booking': booking}
    return render(request, 'book_property/booking_history.html', context)

@login_required
def profile(request, username):
    user_profile = get_object_or_404(User_Profile, username=username)
    return render(request, 'profile.html', {'user_profile': user_profile})

def about_us(request):   
    members=Member.objects.get()
    context={'member':members,}
    return render(request, template_name= 'about_us.html',context=context)

def support(request):   
    return render(request, template_name= 'support.html')

