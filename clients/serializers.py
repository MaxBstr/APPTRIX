from rest_framework import serializers

from clients.models import Client, Match


class ClientSerializer(serializers.ModelSerializer):

    email = serializers.EmailField()

    class Meta:
        model = Client
        fields = [
            'username', 'first_name', 'last_name',
            'email', 'avatar', 'gender', 'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'avatar': {'write_only': True}
        }

    def create(self, validated_data):
        client = Client(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            gender=validated_data['gender'],
            avatar=validated_data['avatar']
        )
        client.set_password(validated_data['password'])
        client.save()
        return client

    def validate_email(self, value):
        lower_email = value.lower()
        if Client.objects.filter(email__iexact=lower_email).exists():
            raise serializers.ValidationError('This email is already exists')
        return lower_email


class MatchSerializer(serializers.ModelSerializer):

    sender = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate(self, data):
        if data['sender'] == self.context['recipient']:
            raise serializers.ValidationError('You cannot match yourself')
        return data

    def create(self, validated_data):
        return Match.objects.create(
            sender=validated_data['sender'],
            recipient=self.context['recipient']
        )

    class Meta:
        model = Match
        fields = ['sender']
