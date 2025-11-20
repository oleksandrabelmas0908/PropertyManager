from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

import requests
import os


PARSER_SERVICE_URL = os.getenv("PARSER_SERVICE_URL", "http://nlp:8000")

class InputView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        input_data = request.data.get("input_data")

        response = requests.post(
            url=f"{PARSER_SERVICE_URL}/parse/",
            json={"text": input_data}
        )
        processed_data = response.json()

        return Response(
            {"processed_data": processed_data},
            status=status.HTTP_200_OK
        )