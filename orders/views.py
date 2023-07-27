from django.shortcuts import get_object_or_404
from rest_framework import generics,status,permissions
from rest_framework.response import Response
from .models import Order
#from authentication.models import User
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from .serializers import OrderCreationSerializer,OrderDetailSerializer,StatusUpdateSerializer

User = get_user_model()

class HelloOrderView(generics.GenericAPIView):
    def get(self,request):
        return Response(data={"message":"Hello order"},status=status.HTTP_200_OK)


class OrderCreateListView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = OrderCreationSerializer
    queryset = Order.objects.all()

    @swagger_auto_schema(operation_summary = 'List of Orders')
    def get(self,request):
        orders = Order.objects.all()
        serializer = self.serializer_class(instance=orders,many=True)

        return Response(data=serializer.data,status=status.HTTP_200_OK)
    
    @swagger_auto_schema(operation_summary = 'Create an Order')
    def post(self,request):
        data=request.data
        serializer = self.serializer_class(data=data)
        user = request.user

        if serializer.is_valid():
            serializer.save(customer=user)

            return Response(data=serializer.data,status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class OrderDetailView(generics.GenericAPIView):
    serializer_class = OrderDetailSerializer
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(operation_summary = 'Get an Order')
    def get(self,request,pk):
        order =get_object_or_404(Order,pk=pk)
        serializer = self.serializer_class(instance=order)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    
    @swagger_auto_schema(operation_summary = 'Update an Order')                
    def put(self,request,pk):
        data = request.data
        order = get_object_or_404(Order,pk=pk)
        serializer = self.serializer_class(data=data,instance=order)
        #user = request.user

        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data,status=status.HTTP_200_OK)
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(operation_summary = 'Delete an Order')
    def delete(self,request,pk):
        order =get_object_or_404(Order,pk=pk)

        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class UpdateOrderStatus(generics.GenericAPIView):
    serializer_class = StatusUpdateSerializer
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAdminUser]

    def put(self,request,pk):
       data = request.data
       order = get_object_or_404(Order,pk=pk) 
       serializer = self.serializer_class(data=data,instance=order)
       if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data,status=status.HTTP_200_OK)
       return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class UserOrderView(generics.GenericAPIView):
    serializer_class = OrderDetailSerializer
    queryset = Order.objects.all()

    def get(self,request,user_id):
        user = User.objects.get(pk=user_id)
        order = Order.objects.all().filter(customer=user)
        serializer = self.serializer_class(instance=order,many=True)

        return Response(data=serializer.data,status=status.HTTP_200_OK)

class UserOrderDetail(generics.GenericAPIView):
    serializer_class = OrderDetailSerializer
    queryset = Order.objects.all()

    def get(self,request,user_id,order_id):
        user = User.objects.get(pk=user_id)
        order = Order.objects.all().filter(customer=user).get(pk=order_id)
        serializer = self.serializer_class(instance=order)

        return Response(data=serializer.data,status=status.HTTP_200_OK)