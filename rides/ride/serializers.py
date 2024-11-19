from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Ride, RideEvent


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number']  # Include phone_number if added via custom user model


# RideEvent Serializer
class RideEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideEvent
        fields = ['id', 'id_ride', 'description', 'created_at']


# Ride Serializer
class RideSerializer(serializers.ModelSerializer):
    rider = UserSerializer(source='id_rider', read_only=True)
    driver = UserSerializer(source='id_driver', read_only=True)
    ride_events = RideEventSerializer(source='rideevent_set', many=True, read_only=True)
    todays_ride_events = serializers.SerializerMethodField()

    class Meta:
        model = Ride
        fields = [
            'id_ride', 'status', 'pickup_latitude', 'pickup_longitude',
            'dropoff_latitude', 'dropoff_longitude', 'pickup_time',
            'rider', 'driver', 'ride_events', 'todays_ride_events'
        ]

    def get_todays_ride_events(self, obj):
        from django.utils.timezone import now, timedelta
        last_24_hours = now() - timedelta(hours=24)
        events = obj.rideevent_set.filter(created_at__gte=last_24_hours)
        return RideEventSerializer(events, many=True).data
