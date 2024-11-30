from django.forms import ModelForm
from .models import *
class PropertyForm(ModelForm):
    class Meta:
        model = Property
        fields = ['property_type', 'location', 'description', 'num_of_rooms', 'num_of_bathrooms', 'area_size', 'price', 'address', 'status', 'image_1', 'image_2', 'image_3']

class UserForm(ModelForm):
    class Meta:
        model=User_Profile
        fields = ['email', 'phone', 'address', 'profile_image']