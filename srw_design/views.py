from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RetainingWallSerializer
from .utils.stability_check import stability_check
from .utils.plotters import plot_wall

class RetainingWallAPIView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = RetainingWallSerializer(data=request.data)
        if serializer.is_valid():
            wall_properties = serializer.data
            stability_results = stability_check(**wall_properties)
            img_path = plot_wall( **wall_properties, **stability_results)  # Make sure your plot_wall function saves the plot as an image and returns its path.

            return Response({'img_path': img_path, 'stability_results': stability_results})

        return Response(serializer.errors, status=400)