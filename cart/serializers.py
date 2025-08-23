from rest_framework import serializers
from .models import CartItem, Cart
from shop.serializers import ProductSerializer, CustomDesignSerializer, UserSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True, required=False)
    custom_design = CustomDesignSerializer(read_only=True)
    custom_design_id = serializers.IntegerField(write_only=True, required=False)
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = CartItem
        fields = '__all__'
        read_only_fields = ['user', 'added_at']
    
    def get_total_price(self, obj):
        return obj.total_price()
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    def validate(self, attrs):
        if not attrs.get('product_id') and not attrs.get('custom_design_id'):
            raise serializers.ValidationError("Either product_id or custom_design_id must be provided")
        return attrs


class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    subtotal = serializers.SerializerMethodField()
    discount = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    item_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']
    
    def get_subtotal(self, obj):
        return obj.get_subtotal()
    
    def get_discount(self, obj):
        return obj.get_discount()
    
    def get_total(self, obj):
        return obj.get_total()
    
    def get_item_count(self, obj):
        return obj.get_item_count()
