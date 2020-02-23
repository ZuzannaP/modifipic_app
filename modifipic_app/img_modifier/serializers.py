from rest_framework import serializers
from .models import TheImage


class ImageSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='get_category_display')

    class Meta:
        model = TheImage
        fields = ['pk', 'file', 'category', 'upload_date']
