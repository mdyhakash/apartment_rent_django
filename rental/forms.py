from django.forms import ModelForm
from django import forms
from .models import *
class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['property_type', 'location', 'description', 'num_of_rooms', 'num_of_bathrooms', 'area_size', 'price', 'address', 'status', 'image_1', 'image_2', 'image_3']
        widgets = {
            'property_type': forms.TextInput(attrs={'class': 'w-full py-2 px-4 border border-gray-300 rounded-lg'}),
            'location': forms.TextInput(attrs={'class': 'w-full py-2 px-4 border border-gray-300 rounded-lg'}),
            'description': forms.Textarea(attrs={'class': 'w-full py-2 px-4 border border-gray-300 rounded-lg', 'rows': 3}),
            'num_of_rooms': forms.NumberInput(attrs={'class': 'w-full py-2 px-4 border border-gray-300 rounded-lg'}),
            'num_of_bathrooms': forms.NumberInput(attrs={'class': 'w-full py-2 px-4 border border-gray-300 rounded-lg'}),
            'area_size': forms.NumberInput(attrs={'class': 'w-full py-2 px-4 border border-gray-300 rounded-lg'}),
            'price': forms.NumberInput(attrs={'class': 'w-full py-2 px-4 border border-gray-300 rounded-lg'}),
            'address': forms.Textarea(attrs={'class': 'w-full py-2 px-4 border border-gray-300 rounded-lg', 'rows': 2}),
            'status': forms.Select(attrs={'class': 'w-full py-2 px-4 border border-gray-300 rounded-lg'}),
            'image_1': forms.FileInput(attrs={'class': 'w-full py-2 px-4 border border-gray-300 rounded-lg'}),
            'image_2': forms.FileInput(attrs={'class': 'w-full py-2 px-4 border border-gray-300 rounded-lg'}),
            'image_3': forms.FileInput(attrs={'class': 'w-full py-2 px-4 border border-gray-300 rounded-lg'}),
        }

class UserForm(ModelForm):
    class Meta:
        model=User_Profile
        fields = ['email', 'phone', 'address', 'profile_image']