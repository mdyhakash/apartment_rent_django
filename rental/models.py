from django.db import models


class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    user_type = models.CharField(max_length=50)
    join_date=models.DateField()
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)

    def __str__(self):
        return self.username

class Property(models.Model):
    property_type = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    description = models.TextField()
    num_of_rooms = models.IntegerField()
    num_of_bathrooms = models.IntegerField()
    area_size = models.FloatField()
    price = models.FloatField()
    status = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    image_1 = models.ImageField(upload_to='property_images/', null=True, blank=True)
    image_2 = models.ImageField(upload_to='property_images/', null=True, blank=True)
    image_3 = models.ImageField(upload_to='property_images/', null=True, blank=True)
    image_4 = models.ImageField(upload_to='property_images/', null=True, blank=True)
    image_5 = models.ImageField(upload_to='property_images/', null=True, blank=True)
    image_6 = models.ImageField(upload_to='property_images/', null=True, blank=True)
    image_7 = models.ImageField(upload_to='property_images/', null=True, blank=True)
     
    def __str__(self):
        return self.property_type

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    booking_date = models.DateTimeField()
    date_created = models.DateTimeField(auto_now_add=True)
