from rest_framework import serializers
from .models import Image


class ImageSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='get_category_display')

    class Meta:
        model = Image
        fields = ['pk', 'file', 'category', 'upload_date']
