from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register([User_Profile,Property,Booking,Member,Comment,Rating,Payment])
