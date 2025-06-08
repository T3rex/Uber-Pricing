# pricing_engine/serializers.py
from rest_framework import serializers
from .models import Ride
from django.utils import timezone

class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = '__all__'
        read_only_fields = ['calculated_price']
    
    def validate(self, data):
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        total_distance = data.get('total_distance')
        waiting_time = data.get('waiting_time_minutes')

        
        if end_time and start_time and end_time <= start_time:
            raise serializers.ValidationError("End time must be after start time.")

        if total_distance is not None and total_distance < 0:
            raise serializers.ValidationError("Total distance must be >= 0.")

        if waiting_time is not None and waiting_time < 0:
            raise serializers.ValidationError("Waiting time must be >= 0.")
        
        #waiting time can not exceed total ride time
        if start_time and end_time and waiting_time is not None:
            total_ride_time = int((end_time - start_time).total_seconds() / 60)
            if waiting_time > total_ride_time:
                raise serializers.ValidationError("Waiting time cannot exceed total ride time.")
            
        #start time can not be in future      
        if start_time and start_time > timezone.now():
            raise serializers.ValidationError("Start time cannot be in the future.")

        return data
