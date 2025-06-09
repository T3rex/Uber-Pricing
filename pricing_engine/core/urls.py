# pricing_engine/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('api/rides/', views.RideCreateAPIView.as_view(), name='ride-create'),   
    path('', views.ride_view, name='ride-form'),
    path('ride_detail/<int:pk>/', views.ride_detail, name='ride_detail'),
]
