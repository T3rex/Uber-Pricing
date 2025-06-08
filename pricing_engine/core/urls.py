# pricing_engine/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('api/rides/', views.RideCreateAPIView.as_view(), name='ride-create'),   
]
