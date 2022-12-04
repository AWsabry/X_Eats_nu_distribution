from rest_framework import serializers
from .models import Order,Cart,CartItems




class CartItems_Serializer(serializers.ModelSerializer):
    class Meta:
        model = CartItems
        fields = ['user',"cart", "orderId","ordered",
        'paid',"product", "price","quantity",
        'created',"totalOrderItemPrice", "Restaurant","order_shift",
        ]

class Cart_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['user',"total_after_delivery", "ordered_date","total_price",]






class Orders_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['user',"total_price_after_delivery", "ordered_date","paid","comment","totalPrice","cart","flag",]

