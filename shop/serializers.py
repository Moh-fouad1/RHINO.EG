from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import Category, Product, CustomDesign, Review, Order, OrderItem, PromoCode
from cart.models import CartItem, Cart


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    final_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = '__all__'
    
    def get_final_price(self, obj):
        return obj.get_final_price()


class CustomDesignSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    design_file_url = serializers.SerializerMethodField()
    calculated_price = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomDesign
        fields = '__all__'
        read_only_fields = ['user', 'status', 'created_at', 'updated_at']
    
    def get_design_file_url(self, obj):
        if obj.design_file:
            return self.context['request'].build_absolute_uri(obj.design_file.url)
        return None
    
    def get_calculated_price(self, obj):
        return obj.calculate_price()
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['user', 'is_approved', 'created_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['user', 'order_number', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class PromoCodeSerializer(serializers.ModelSerializer):
    is_valid = serializers.SerializerMethodField()
    
    class Meta:
        model = PromoCode
        fields = '__all__'
    
    def get_is_valid(self, obj):
        return obj.is_valid()


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
