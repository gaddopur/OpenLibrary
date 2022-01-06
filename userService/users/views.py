from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CustomUserSerializer
from .producer import publish

CustomUser = get_user_model()

# Create your views here.
class UserAPIView(APIView):
    def get(self, request):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            publish('user_created', serializer.data['id'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailAPIView(APIView):
    def get_user(self, pk):
        try:
            user = CustomUser.objects.get(pk=pk)
            return user
        except:
            return False

    def get(self, request, pk):
        user = self.get_user(pk)
        if user:
            serializer = CustomUserSerializer(user)
            return Response(serializer.data)
        return Response("user does not exist!", status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, pk):
        user = self.get_user(pk)
        if user:
            serializer = CustomUserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response("user does not exist!", status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        user = self.get_user(pk)
        try:
            user.delete()
            publish('user_deleted', pk)
            return Response("user deleted sucessfully", status=status.HTTP_204_NO_CONTENT)
        except:
            return Response("user does not exist!", status=status.HTTP_404_NOT_FOUND)
