from datetime import date
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
from broker import get_messages, produce


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")


PARSER_SERVICE_URL = os.getenv("PARSER_SERVICE_URL", "http://nlp:8000")
MATCHING_SERVICE_URL = os.getenv("MATCHING_SERVICE_URL", "http://matching-service:8000")


class InputView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InputDataSerializer
    
    def post(self, request):
        input_data = request.data.get("input_data")
        
        try:
            produce(message=input_data, topic="send_to_parse_topic")

            status_data = requests.get(url=f"{PARSER_SERVICE_URL}/parse/") 

            messages = get_messages(topic="parsed_data_topic", group_id="api_service_group")
            if not messages:
                logger.info("No messages received from 'parsed_data_topic'.")
                return Response(
                    {"message": "no processed messages"},
                    status=status.HTTP_200_OK
                )
        except Exception as e:
            logger.error(f"Error in processing input data: {e}")
            return Response(
                {"error": e},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
        processed_messages = []
        for processed_data in messages:
            try:

                user = User.objects.get(email=processed_data["email"])
                if user:
                    logger.info(f"User with email {processed_data['email']} already exists. Skipping.")
                    continue

                city = City.objects.get_or_create(name=processed_data["city"])[0]
                
                city_id = city.id
                processed_data["city"] = city_id

                processed_data["day_of_moving_in"] = date.fromisoformat(processed_data["day_of_moving_in"])

                serializer = UserSerializerIn(data=processed_data)
                serializer.is_valid(raise_exception=True)
                serializer.save()

                processed_messages.append(serializer.data)

            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(
            {"processed_data": processed_messages},
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
            produce(message={"user_id": int(user_id)}, topic="match_topic")
            status_match = requests.get(
                url=f"{MATCHING_SERVICE_URL}/match/"
            )
            matched_properties = get_messages(
                topic="proceeded_match_topic",
                group_id="api_service_match_group"
            )
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
