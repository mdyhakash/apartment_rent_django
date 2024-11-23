from django.db import models
from django.contrib.auth.models import User

class User_Profile(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    user_type = models.CharField(max_length=50)
    join_date=models.DateField()
    address=models.TextField(max_length=200, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True,default='profiles/default_profile.png')

    def __str__(self):
        return self.username

class Property(models.Model):
    STATUS_CHOICES = [
        ('booked', 'Booked'),
        ('not_booked', 'Not Booked'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
        ('available', 'Available'),
        ('reserved', 'Reserved'),
    ]

    property_type = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    description = models.TextField()
    num_of_rooms = models.IntegerField()
    num_of_bathrooms = models.IntegerField()
    area_size = models.FloatField()
    price = models.FloatField()
    address = models.TextField(max_length=200, blank=True, null=True)
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='not_booked'
    )
    date_created = models.DateTimeField(auto_now_add=True)
    image_1 = models.ImageField(upload_to='property_images/', null=True, blank=True,default='property_images/default_property.png')
    image_2 = models.ImageField(upload_to='property_images/', null=True, blank=True)
    image_3 = models.ImageField(upload_to='property_images/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.property_type}"


class Booking(models.Model):
    user = models.ForeignKey(User_Profile, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    booking_date = models.DateTimeField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)