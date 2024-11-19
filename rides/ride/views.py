from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .models import Ride, RideEvent
from .serializers import RideSerializer, RideEventSerializer, UserProfileSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Prefetch
from django.conf import settings
from django.apps import apps
from geopy.distance import geodesic
from .decorators import admin_only  # Import the admin_only decorator

# Dynamically load the custom user model
User = apps.get_model(settings.AUTH_USER_MODEL)

# Custom Pagination
class StandardResultsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# Ride ViewSet (Manually defining actions)
class RideViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'id_rider__email']
    ordering_fields = ['pickup_time']

    def get_queryset(self):
        return Ride.objects.prefetch_related(
            Prefetch('rideevent_set'),
            'id_rider',
            'id_driver'
        )

    @admin_only  # Apply the admin_only decorator
    def list(self, request):
        rides = self.get_queryset()
        latitude = float(request.query_params.get('latitude', 0))
        longitude = float(request.query_params.get('longitude', 0))
        for ride in rides:
            pickup_location = (ride.pickup_latitude, ride.pickup_longitude)
            ride.distance_to_pickup = geodesic((latitude, longitude), pickup_location).km

        sorted_rides = sorted(rides, key=lambda r: r.distance_to_pickup)
        page = self.paginate_queryset(sorted_rides)
        if page is not None:
            serializer = RideSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = RideSerializer(sorted_rides, many=True)
        return Response(serializer.data)

    @admin_only  # Apply the admin_only decorator
    def retrieve(self, request, pk=None):
        try:
            ride = Ride.objects.prefetch_related(
                Prefetch('rideevent_set'),
                'id_rider',
                'id_driver'
            ).get(pk=pk)
            serializer = RideSerializer(ride)
            return Response(serializer.data)
        except Ride.DoesNotExist:
            return Response({"error": "Ride not found"}, status=404)

    @admin_only  # Apply the admin_only decorator
    @action(detail=False, methods=['get'])
    def sort_by_distance(self, request):
        try:
            latitude = float(request.query_params.get('latitude'))
            longitude = float(request.query_params.get('longitude'))
        except (TypeError, ValueError):
            return Response({"error": "Invalid GPS coordinates. Please provide valid latitude and longitude values."},
                            status=400)

        rides = self.get_queryset()
        for ride in rides:
            pickup_location = (ride.pickup_latitude, ride.pickup_longitude)
            ride.distance_to_pickup = geodesic((latitude, longitude), pickup_location).km

        sorted_rides = sorted(rides, key=lambda r: r.distance_to_pickup)
        page = self.paginate_queryset(sorted_rides)
        if page is not None:
            serializer = RideSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = RideSerializer(sorted_rides, many=True)
        return Response(serializer.data)

# RideEvent ViewSet (Manually defining actions)
class RideEventViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @admin_only  # Apply the admin_only decorator
    def list(self, request):
        queryset = RideEvent.objects.all()
        serializer = RideEventSerializer(queryset, many=True)
        return Response(serializer.data)

    @admin_only  # Apply the admin_only decorator
    def retrieve(self, request, pk=None):
        try:
            ride_event = RideEvent.objects.get(pk=pk)
            serializer = RideEventSerializer(ride_event)
            return Response(serializer.data)
        except RideEvent.DoesNotExist:
            return Response({"error": "RideEvent not found"}, status=404)

# User ViewSet (Manually defining actions)
class UserViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @admin_only  # Apply the admin_only decorator
    def list(self, request):
        queryset = User.objects.all()
        serializer = UserProfileSerializer(queryset, many=True)
        return Response(serializer.data)

    @admin_only  # Apply the admin_only decorator
    def retrieve(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            serializer = UserProfileSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
