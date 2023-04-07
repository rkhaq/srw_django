from rest_framework import serializers
from .models import RetainingWall

class RetainingWallSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetainingWall
        fields = '__all__'
