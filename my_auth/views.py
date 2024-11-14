from django.shortcuts import render

# Create your views here.
def login(request):
    return render(request, template_name="login.html")

def register(request):
   return render(request, template_name="register.html")