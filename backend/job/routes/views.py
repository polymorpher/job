import requests
import json

from django.http import HttpResponse
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response



def ping(request):
    data = {status: True}
    return HttpResponse("pong", content_type="text/plain")


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def bang(request):
    data = {status: True}
    return Response(status=status.HTTP_200_OK, data=data)