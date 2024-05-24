from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('startDb', views.startDb, name='landing'),
    path('compare',views.compare,name='compare'),
    path('mobile/<int:page>',views.getMobilePhones,name='getMobilePhones'),
    path('tablet/<int:page>',views.getTablets,name='getTablets'),
    path('tvs/<int:page>',views.getTvs,name='getTVs'),
    path('speakers/<int:page>',views.getSpeakers,name='getSpeakers'),
    path('getdetails/<str:name>',views.getDetails,name='getDetails'),
    path('powerbank/<int:page>',views.getPowerBanks,name='getPowerBanks'),
    path('smartwatch/<int:page>',views.getSmartWatches,name='getSmartWatches'),
    path('laptops/<int:page>',views.getLaptops,name='getLaptops'),
    path('earbuds/<int:page>',views.getEarbuds,name='getEarbuds'),
    path('explore',views.explore,name='explore'),
    path('explore/<int:page>',views.explore,name='explore'),
    path('product/<int:id>',views.productDetails,name='product'),
    path('allproductnames/<str:category>/', views.allProdNames, name='allProdNamesByCategory'),
    path('allproductnames',views.allProdNames,name='allProdNames'),

    path('addReview/<int:id>',views.addReview,name='addReview'),




]
