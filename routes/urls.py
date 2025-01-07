from django.urls import path
from .views import RoutePlannerAPIView

urlpatterns = [
    path('route/', RoutePlannerAPIView.as_view(), name='route-planner'),
]
