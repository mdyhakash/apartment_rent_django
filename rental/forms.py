from django.forms import ModelForm
from .models import *
class PropertyForm(ModelForm):
    class Meta:
        model = Property
        fields = '__all__'

class UserForm(ModelForm):
    class Meta:
        model=User
        fields='__all__'