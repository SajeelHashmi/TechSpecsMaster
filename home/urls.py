from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'home'  # This defines the namespace for this URLconf

urlpatterns = [
    path('', views.home, name='home'),
    path('contact', views.contact, name="contact"),
    path('wishlist/<int:id>', views.addToWishlist, name="addToWishlist"),
    path('removeFromWishlist/<int:id>', views.removeFromWishlist, name="removeFromWishlist"),
    path('dashboard',views.dashboard,name = "dashboard"),

    path('about', views.about, name="about"),

    path('getInTouch',views.getInTouch,name = "getInTouch"),



]
