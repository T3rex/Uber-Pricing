# pricing_engine/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Ride
from .serializers import RideSerializer
from django.shortcuts import render,redirect
from .forms import RideForm
from django.contrib import messages


class RideCreateAPIView(APIView):
    def post(self, request):
        serializer = RideSerializer(data=request.data)
        if serializer.is_valid():
            ride = serializer.save()
            ride.calculate_price()
            ride.save()
            return Response(RideSerializer(ride).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

def ride_view(request):
    if request.method == 'POST':
        form = RideForm(request.POST)
        if form.is_valid():
            ride = form.save(commit=False)
            ride.created_by = request.user
            ride.updated_by = request.user
            ride.calculate_price()
            ride.save()
            messages.success(request, 'Ride created successfully!')
            return redirect('ride_detail', pk=ride.pk)
    else:
        form = RideForm()
    
    return render(request, 'ride_form.html', {'form': form})

def ride_detail(request, pk):    
    ride = Ride.objects.get(pk=pk)    
    return render(request, 'ride_detail.html', {'ride': ride})