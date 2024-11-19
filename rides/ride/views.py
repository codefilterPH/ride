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

# Dynamically load the custom user model
User = apps.get_model(settings.AUTH_USER_MODEL)


# Custom Pagination
class StandardResultsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


# Ride ViewSet
class RideViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [permissions.IsAuthenticated]  # Admin-only handled in permission logic
    pagination_class = StandardResultsPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'id_rider__email']
    ordering_fields = ['pickup_time']

    def get_queryset(self):
        # Optimize with prefetching for performance
        return Ride.objects.prefetch_related(
            Prefetch('rideevent_set'),
            'id_rider',
            'id_driver'
        )

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
        page = self.paginate_queryset(sorted_rides)  # Paginate sorted rides
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # If no pagination is required (i.e., when all results are returned at once)
        serializer = self.get_serializer(sorted_rides, many=True)
        return Response(serializer.data)


# RideEvent ViewSet
class RideEventViewSet(viewsets.ModelViewSet):
    queryset = RideEvent.objects.all()
    serializer_class = RideEventSerializer
    permission_classes = [permissions.IsAuthenticated]


# User ViewSet
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()  # Now this will work
    serializer_class = UserProfileSerializer
