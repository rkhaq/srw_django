from django.urls import path
from .views import RetainingWallAPIView, get_wall_image, hello_api

urlpatterns = [
    path('api/hello/', hello_api, name='hello_api'),
    path('api/retaining_wall/', RetainingWallAPIView.as_view(), name='retaining_wall_api'),
    path('api/retaining_wall_image/<str:cache_key>/', get_wall_image, name='get_wall_image'),
]
