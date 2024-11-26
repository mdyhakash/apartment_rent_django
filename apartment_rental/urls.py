from django.contrib import admin
from django.urls import path
from . import settings
from django.conf.urls.static import static
from rental import views as prop_views
from my_auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', prop_views.home, name="home"),
    path('login/', prop_views.login, name='login'),
    path('register/', prop_views.register, name='register'),
    path('signout/',prop_views.signout,name='signout'),
    path('property/', prop_views.property, name='property'),
    path('add_property/', prop_views.add_property, name='add_property'),
    path('update_property/<str:id>',prop_views.update_property,name='update_property'),
    path('delete_property/<str:id>',prop_views.delete_property,name='delete_property'),
    path('propertydetails/<str:id>',prop_views.propertydetails,name='propertydetails'),
    path('book_property/<str:id>', prop_views.book_property, name='book_property'),
    path('booking_success/<str:id>', prop_views.booking_success, name='booking_success'),
    path('profile/<str:username>', prop_views.profile, name='profile'),
    # user

    path('add_user/',prop_views.add_user,name='add_user'),
    path('user/',prop_views.user,name='user'),
    path('update_user/<str:id>',prop_views.update_user,name='update_user'),
    path('delete_user/<str:id>',prop_views.delete_user,name='delete_user'),
    
    # booking
    path('booking_history/', prop_views.booking_history, name='booking_history')

]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)