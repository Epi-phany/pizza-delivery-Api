from rest_framework import generics,status,permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from django.contrib.auth import authenticate
from .serializers import UserCreationSerializer,UserListSerializer,LogInSerializer
from drf_yasg.utils import swagger_auto_schema

class UserView(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    
    @swagger_auto_schema(operation_summary = 'User List')
    def get(self,request):
        user = User.objects.all()
        serializer = self.serializer_class(instance=user,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    

class UserCreateView(generics.GenericAPIView):

    serializer_class = UserCreationSerializer

    @swagger_auto_schema(operation_summary = 'User create api')
    def post(self,request):
        data= request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

        

