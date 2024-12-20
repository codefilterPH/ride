from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RideViewSet, RideEventViewSet, UserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Initialize the router
router = DefaultRouter()
router.register(r'rides', RideViewSet, basename='ride')
router.register(r'ride-events', RideEventViewSet, basename='ride_event')
router.register(r'users', UserViewSet, basename='user')

# Define the URL patterns
urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),  # API base path
]
# NOTES
"""
List all rides: /api/rides/
Retrieve a specific ride: /api/rides/<pk>/
Sort rides by distance: /api/rides/sort_by_distance/

List all ride events: /api/ride-events/
Retrieve a specific ride event: /api/ride-events/<pk>/

List all users: /api/users/
Retrieve a specific user: /api/users/<pk>/
"""