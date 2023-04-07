from django.urls import path
from .views import RetainingWallAPIView

urlpatterns = [
    path('api/retaining_wall/', RetainingWallAPIView.as_view(), name='retaining_wall_api'),
]
