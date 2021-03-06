from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.generics import CreateAPIView, ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status

from clients.serializers import ClientSerializer, MatchSerializer
from clients.models import Client, Match
from clients.utils import send_mail
from clients.filters import ClientFilter


class CreateClientAPIView(CreateAPIView):
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


class GetClientListAPIView(ListAPIView):
    """
        Returns list with filtering capability
        Available filter fields:
            gender, first_name, last_name, distance
    """

    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filter_class = ClientFilter


class CreateMatchAPIView(CreateAPIView):
    """
        Handling matches -> creates Match object
        If double match -> send message on email to both
        participants
    """

    permission_classes = [IsAuthenticated]
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

    def create(self, request, *args, **kwargs):
        sender = request.user
        recipient = Client.objects.get(pk=kwargs['pk'])
        serializer = MatchSerializer(
            data={**request.data},
            context={
                'request': request,
                'recipient': recipient
            }
        )

        if serializer.is_valid(raise_exception=True):
            serializer.save()

        if Match.objects.filter(sender=recipient, recipient=sender).exists():
            send_mail(sender, recipient)
            send_mail(recipient, sender)
            response_data = {
                'match': True,
                'participant': recipient.username,
                'email': recipient.email,
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            response_data = {
                'participant': recipient.username,
                'status': 'sent match'
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
