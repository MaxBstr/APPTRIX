from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from clients.serializers import ClientSerializer
from clients.models import Client


class ClientCreateAPIView(CreateAPIView):
    """
        Creates user and generating auth token
    """
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    parser_classes = [FormParser, MultiPartParser]
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            new_client = serializer.save()
            token = Token.objects.create(user=new_client).key
            response_data = {
                'user': new_client.username,
                'token': token,
                'status': 'created'
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailClientAPIView(RetrieveAPIView):
    """
        Get Client info
    """
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]
    queryset = Client.objects.all()
