from django.contrib import admin
from django.urls import path
from . import settings
from django.conf.urls.static import static
from rental import views as prop_views
#from auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', prop_views.home, name="home"),
    #path('login/', auth_views.login, name='login'),
    #path('register/', auth_views.register, name='register'),
    path('property/', prop_views.property, name='property'),
    path('add_property/', prop_views.add_property, name='add_property'),
    path('update_property/<str:id>',prop_views.update_property,name='update_property'),
    path('delete_property/<str:id>',prop_views.delete_property,name='delete_property'),
    path('propertydetails/<str:id>',prop_views.propertydetails,name='propertydetails'),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
