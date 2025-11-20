from rest_framework import serializers
from main_service.models import User


class UserSerializerIn(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "phone",
            "first_name",
            "last_name",
            "bedrooms",
            "max_budget",
            "monthly_income",
            "city",
            "day_of_moving_in",
            "pets",
            "pool",
            "yard",
            "parking",
        )