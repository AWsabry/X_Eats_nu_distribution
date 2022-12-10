from rest_framework import serializers
from .models import Order,Cart,CartItems




class CartItems_Serializer(serializers.ModelSerializer):
    class Meta:
        model = CartItems
        fields = '__all__'

class Cart_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class Orders_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

