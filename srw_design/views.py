from rest_framework.views import APIView
from rest_framework.response import Response

from django.http import JsonResponse
from django.core.cache import cache

from .serializers import RetainingWallSerializer
from .utils.stability_check import stability_check
from .utils.plotters import plot_wall

class RetainingWallAPIView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = RetainingWallSerializer(data=request.data)
        if serializer.is_valid():
            wall_properties = serializer.data
            stability_results = stability_check(**wall_properties)
            plot_cache_key = plot_wall( **wall_properties, **stability_results)  # Make sure your plot_wall function saves the plot as an image and returns its path.

            return Response({'plote_cache_key': plot_cache_key, 'stability_results': stability_results})

        return Response(serializer.errors, status=400)

def get_wall_image(request, cache_key):
    image_data = cache.get(cache_key)

    if image_data is not None:
        return JsonResponse({'image_data': image_data})
    else:
        return JsonResponse({'error': 'Image not found or expired'}, status=404) 
    
def hello_api(request):
    return JsonResponse({'message': 'hello'})