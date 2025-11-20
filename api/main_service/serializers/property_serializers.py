from rest_framework import serializers
from main_service.models import Property


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = (
            "id",
            "title",
            "description",
            "price",
            "bedrooms",
            "address",
            "city",
        )