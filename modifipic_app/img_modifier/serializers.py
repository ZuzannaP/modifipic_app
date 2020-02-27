from rest_framework import serializers
from .models import TheImage


class ImageSerializer(serializers.ModelSerializer):
    category = serializers.CharField(max_length=128)

    class Meta:
        model = TheImage
        fields = ['pk', 'file', 'category', 'upload_date']
