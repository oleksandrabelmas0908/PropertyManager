from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

import requests
import os

from main_service.serializers.user_serializers import InputDataSerializer, UserSerializerIn
from main_service.models import City


PARSER_SERVICE_URL = os.getenv("PARSER_SERVICE_URL", "http://nlp:8000")


class InputView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InputDataSerializer
    
    def post(self, request):
        input_data = request.data.get("input_data")

        response = requests.post(
            url=f"{PARSER_SERVICE_URL}/parse/",
            json={"input_data": input_data}
        )
        processed_data = response.json()

        try:
            city = City.objects.get_or_create(name=processed_data["city"])
            city_id = city[0].id
            processed_data["city"] = city_id

            serializer = UserSerializerIn(data=processed_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()


        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"processed_data": serializer.data},
            status=status.HTTP_200_OK
        )