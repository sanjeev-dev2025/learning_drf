from django.contrib import admin
from django.urls import path
from apiapp import views

urlpatterns = [
   path('products/',views.ProductListCreateAPIView.as_view()),
   path('products/<int:pk>/update/',views.ProductRetrieveUpdateDestroyAPIView.as_view()),
   path('orders/',views.OrderListCreateAPIView.as_view()),
   path('order_items/',views.OrderItemListAPIView.as_view()),
   path('product_info/',views.ProductInfoAPIView.as_view()),
   path('userorders/',views.UserOrderListAPIView.as_view(),name='userorders'),
   path('exportcsv/',views.ExportProductCSVAPIView,name='exportcsv'),
   path('userorders/<int:pk>/',views.OrderDestroy.as_view()),
]
