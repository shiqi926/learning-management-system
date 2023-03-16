from .helpers.basic_crud import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from ..serializers import *


@api_view(['GET'])
def get_user_by_username(request, username):
    """
    Retrieve user by username
    """
    try:
        user = Profile.objects.filter(pk=username)
        serializer = ProfileSerializer(user, context={'request': request}, many=True)
        if serializer.data != []:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
    except:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
