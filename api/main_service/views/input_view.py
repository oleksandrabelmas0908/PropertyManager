from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

import requests
import os
import logging

from main_service.serializers.user_serializers import InputDataSerializer, UserSerializerIn
from main_service.models import City, User


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


PARSER_SERVICE_URL = os.getenv("PARSER_SERVICE_URL", "http://nlp:8000")
MATCHING_SERVICE_URL = os.getenv("MATCHING_SERVICE_URL", "http://matching-service:8000")


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
    

class MatchView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='user_id',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                required=True,
                description='ID of the user to fetch matching properties for'
            )
        ],
        responses={200: dict, 400: dict, 500: dict}
    )
    def get(self, request):
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response(
                {"error": "user_id query parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = User.objects.get(id=user_id)
        if not user:
            return Response(
                {"error": f"User with ID {user_id} does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        matches = user.get_matched_properties()
        if matches:
            logger.info(f"Returning cached matched properties for User ID {matches}")
            return Response(
                {"matched_properties": matches},
                status=status.HTTP_200_OK
            )
        else:
            logger.info(f"No matches: {matches}")
        
        try:
            response = requests.post(
                url=f"{MATCHING_SERVICE_URL}/match/",
                json={"user_id": int(user_id)}
            )
            matched_properties = response.json()
        except Exception as e:
            logger.error(f"Error fetching matched properties: {e}")
            return Response(
                {"error": "Failed to fetch matched properties"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            {"matched_properties": matched_properties},
            status=status.HTTP_200_OK
        )
