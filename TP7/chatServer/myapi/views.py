from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializers import MessageSerializer, UserSerializer
from .models import Message

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('source')
    serializer_class = MessageSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer