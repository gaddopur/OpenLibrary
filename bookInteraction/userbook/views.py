from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from .producer import publish
from .serializers import BookUserSerializer
from .models import BookUser, User

# Create your views here.
class BookUserAPIView(viewsets.ViewSet):
    def valid_user(self, request):
        try:
            User.objects.get(userid=request.data['userid'])
            try:
                instance = BookUser.objects.get(userid=request.data['userid'], bookid=request.data['bookid'])
            except BookUser.DoesNotExist:
                instance = BookUser(userid=request.data['userid'], bookid=request.data['bookid'])
            return instance
        except:
            return False

    def like(self, request):
        serializer = BookUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        instance = self.valid_user(request)
        if instance:
            if instance.like == False:
                instance.like = True
                instance.save()
                publish('liked', request.data['bookid'])
                return Response(BookUserSerializer(instance).data, status=status.HTTP_200_OK)
            return Response("User already liked this book!", status=status.HTTP_400_BAD_REQUEST)
        
        return Response("please make sure userid exist!", status=status.HTTP_400_BAD_REQUEST)

    def read(self, request):
        serializer = BookUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        instance = self.valid_user(request)
        if instance:
            if instance.read == False:
                instance.read = True
                instance.save()
                publish('read', request.data['bookid'])
                return Response(BookUserSerializer(instance).data, status=status.HTTP_200_OK)
            return Response("User already read this book!", status=status.HTTP_400_BAD_REQUEST)
        
        return Response("please make sure userid exist!", status=status.HTTP_400_BAD_REQUEST)

