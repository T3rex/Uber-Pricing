# pricing_engine/serializers.py
from rest_framework import serializers
from .models import Ride

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

        return data
