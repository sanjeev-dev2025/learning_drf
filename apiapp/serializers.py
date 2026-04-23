from rest_framework import serializers
from .models import Product,Order,OrderItem

class ProdcutSerializer(serializers.ModelSerializer):
    class Meta:
        model= Product
        fields=(
            'description',
            'name',
            'price',
            'stock',
        ) 

        
    def validate_price(self,value):
        if value<=0:
            raise serializers.ValidationError(' The price must be greater than zero.')
        return value
class OrderSerializer(serializers.ModelSerializer):
    product_name=serializers.SerializerMethodField()
    def get_product_name(self,obj):
            return [item.product.name for item in obj.items.all()]
    products=ProdcutSerializer(many=True,read_only=True)
    total_price=serializers.SerializerMethodField()
    def get_total_price(self, obj):
        order_items=obj.items.all()
        return sum([item.item_subtotal for item in order_items])
    class Meta:
        model=Order
        fields=(
            'order_id',
            'user',
            'created_at',
            'status',
            'product_name',
            'products',
            'total_price',  
           
        )
class OrderItemSerializer(serializers.ModelSerializer):
    product=ProdcutSerializer(read_only=True)
    class Meta:
        model=OrderItem
        
        fields=(
            'order',
            'product',
            'quantity',
                                 
        )
class productinfoserializer(serializers.Serializer):
    product=ProdcutSerializer(many=True)
    count=serializers.IntegerField()
    max_price=serializers.DecimalField(max_digits=10, decimal_places=2)
    