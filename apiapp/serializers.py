from rest_framework import serializers
from apiapp.models import Product,Order,OrderItem

class ProdcutSerializer(serializers.ModelSerializer):
    class Meta:
        model= Product
        fields=(
            'id',
            'name',
            'description',
            'price',
            'stock',
            'image',
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
    
    items_input = serializers.JSONField(write_only=True, required=False)

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
            'items_input',
        )

    def create(self, validated_data):
        items_data = validated_data.pop('items_input', [])
        order = Order.objects.create(**validated_data)
        for item in items_data:
            product_id = item.get('product_id')
            quantity = item.get('quantity', 1)
            try:
                product = Product.objects.get(id=product_id)
                OrderItem.objects.create(order=order, product=product, quantity=quantity)
            except Product.DoesNotExist:
                pass
        return order
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
    