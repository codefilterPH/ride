from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RideViewSet, RideEventViewSet, UserViewSet

router = DefaultRouter()
router.register(r'rides', RideViewSet, basename='ride')
router.register(r'ride-events', RideEventViewSet, basename='ride-event')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]