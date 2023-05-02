from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ValidationError

from app.models import Message, Response


class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class ResponseSerializer(ModelSerializer):
    class Meta:
        model = Response
        fields = '__all__'