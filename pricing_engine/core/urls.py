# pricing_engine/urls.py
from django.urls import path
from .views import RideCreateAPIView

urlpatterns = [
    path('api/rides/', RideCreateAPIView.as_view(), name='ride-create'),
]
