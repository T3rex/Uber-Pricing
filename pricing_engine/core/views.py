# pricing_engine/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Ride
from .serializers import RideSerializer

class RideCreateAPIView(APIView):
    def post(self, request):
        serializer = RideSerializer(data=request.data)
        if serializer.is_valid():
            ride = serializer.save()
            ride.calculate_price()
            ride.save()
            return Response(RideSerializer(ride).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
