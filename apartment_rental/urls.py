from django.contrib import admin
from django.urls import path
from . import settings
from django.conf.urls.static import static
from rental import views as prop_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', prop_views.home, name="home"),
   # path('login/', prop_views.login, name='login'),
   # path('signup/', prop_views.signup, name='signup'),
    path('property/', prop_views.property, name='property'),
    path('propertydetails/<str:p_id>',prop_views.propertydetails,name='propertydetails')
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
