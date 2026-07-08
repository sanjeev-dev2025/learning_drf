from django.http import HttpResponse
from django.db.models import Max
from apiapp.serializers import ProdcutSerializer,OrderSerializer,OrderItemSerializer,productinfoserializer
from apiapp.models import Product,Order,OrderItem,User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from rest_framework import status
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
import csv
from .filters import ProductFilter
# Create your views here.
class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset=Product.objects.all()
    serializer_class=ProdcutSerializer
    
    filterset_class=ProductFilter
    def get_permissions(self):
        self.permission_classes=[AllowAny]
        if self.request.method=='POST':
            self.permission_classes=[IsAdminUser]
        return super().get_permissions()
    
class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Product.objects.all()
    serializer_class=ProdcutSerializer
    
    def get_permissions(self):
        
        if self.request.method== 'PUT' or 'DELETE':
            self.permission_classes=[IsAdminUser]
        return super().get_permissions()  
class OrderListCreateAPIView(generics.ListCreateAPIView):
    queryset=Order.objects.all()
    serializer_class=OrderSerializer
    
    filterset_fields=('user','status')
class UserOrderListAPIView(generics.ListAPIView):
    queryset=Order.objects.all()
    serializer_class=OrderSerializer
    permission_classes=[IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
class OrderItemListAPIView(generics.ListAPIView):
    queryset=OrderItem.objects.all()
    serializer_class=OrderItemSerializer
    filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields=('order','product')

class ProductInfoAPIView(APIView):
     def get(self, request):
         products=Product.objects.all()
         serializer=productinfoserializer({
             'product':products,
             'count':products.count(),
             'max_price':products.aggregate(max_price=Max('price'))['max_price']
         })
         return Response(serializer.data)

def ExportProductCSVAPIView(request):
    products=Product.objects.all()
    response=HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment; filename="products.csv"'
    writer=csv.writer(response)
    writer.writerow(['ID','Name','Description','Price','Stock'])
    for product in products:
        writer.writerow([product.id,product.name,product.description,product.price,product.stock])
    return response