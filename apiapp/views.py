from django.shortcuts import get_object_or_404, render
from django.db.models import Max
from apiapp.serializers import ProdcutSerializer,OrderSerializer,OrderItemSerializer,productinfoserializer
from apiapp.models import Product,Order,OrderItem
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


# Create your views here.
class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset=Product.objects.all()
    serializer_class=ProdcutSerializer

class ProductDestroyAPIView(generics.DestroyAPIView):
    queryset=Product.objects.all()
    serializer_class=ProdcutSerializer
    
class OrderListAPIView(generics.ListAPIView):
    queryset=Order.objects.all()
    serializer_class=OrderSerializer
class UserOrderListAPIView(generics.ListAPIView):
    queryset=Order.objects.all()
    serializer_class=OrderSerializer
    permission_classes=[IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
class OrderItemListAPIView(generics.ListAPIView):
    queryset=OrderItem.objects.all()
    serializer_class=OrderItemSerializer

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset=Product.objects.all()
    serializer_class=ProdcutSerializer


class ProductInfoAPIView(APIView):
     def get(self, request):
         products=Product.objects.all()
         serializer=productinfoserializer({
             'product':products,
             'count':products.count(),
             'max_price':products.aggregate(max_price=Max('price'))['max_price']
         })
         return Response(serializer.data)

