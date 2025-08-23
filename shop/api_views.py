from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import Category, Product, CustomDesign, Review, Order, OrderItem, PromoCode
from .serializers import (
    CategorySerializer, ProductSerializer, CustomDesignSerializer, 
    ReviewSerializer, OrderSerializer, OrderItemSerializer, PromoCodeSerializer,
    UserSerializer, UserRegistrationSerializer
)
from cart.models import CartItem, Cart
from cart.serializers import CartItemSerializer, CartSerializer


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'User registered successfully',
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        """Get all products in a category"""
        category = self.get_object()
        products = Product.objects.filter(category=category, is_active=True)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'framed', 'size', 'featured', 'in_stock']
    search_fields = ['name', 'description', 'category__name']
    ordering_fields = ['name', 'base_price', 'rating', 'created_at', 'sales_count']
    ordering = ['-created_at']

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured products"""
        products = self.queryset.filter(featured=True)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search products"""
        query = request.query_params.get('q', '')
        if query:
            products = self.queryset.filter(
                Q(name__icontains=query) | 
                Q(description__icontains=query) |
                Q(category__name__icontains=query)
            )
        else:
            products = self.queryset.none()
        
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_to_cart(self, request, pk=None):
        """Add product to cart"""
        product = self.get_object()
        quantity = request.data.get('quantity', 1)
        
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': quantity, 'price': product.get_final_price()}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomDesignViewSet(viewsets.ModelViewSet):
    serializer_class = CustomDesignSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'framed', 'size']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return CustomDesign.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def add_to_cart(self, request, pk=None):
        """Add custom design to cart"""
        custom_design = self.get_object()
        custom_design.add_to_cart()
        return Response({'message': 'Custom design added to cart'}, status=status.HTTP_200_OK)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['product', 'rating', 'is_approved']
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']

    def get_queryset(self):
        return Review.objects.filter(is_approved=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status']
    ordering_fields = ['created_at', 'total_amount']
    ordering = ['-created_at']

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel an order"""
        order = self.get_object()
        if order.status in ['pending', 'confirmed']:
            order.status = 'cancelled'
            order.save()
            return Response({'message': 'Order cancelled successfully'})
        return Response({'error': 'Order cannot be cancelled'}, status=status.HTTP_400_BAD_REQUEST)


class PromoCodeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PromoCode.objects.filter(is_active=True)
    serializer_class = PromoCodeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['code', 'description']

    @action(detail=False, methods=['post'])
    def validate(self, request):
        """Validate a promo code"""
        code = request.data.get('code')
        if not code:
            return Response({'error': 'Code is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            promo_code = PromoCode.objects.get(code=code, is_active=True)
            if promo_code.is_valid():
                return Response({
                    'valid': True,
                    'code': PromoCodeSerializer(promo_code).data
                })
            else:
                return Response({
                    'valid': False,
                    'error': 'Promo code is not valid'
                })
        except PromoCode.DoesNotExist:
            return Response({
                'valid': False,
                'error': 'Promo code not found'
            })


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart

    @action(detail=False, methods=['post'])
    def apply_promo(self, request):
        """Apply promo code to cart"""
        cart = self.get_object()
        code = request.data.get('code')
        
        if not code:
            return Response({'error': 'Code is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            promo_code = PromoCode.objects.get(code=code, is_active=True)
            if promo_code.is_valid():
                cart.promo_code = promo_code
                cart.save()
                return Response(CartSerializer(cart).data)
            else:
                return Response({'error': 'Promo code is not valid'}, status=status.HTTP_400_BAD_REQUEST)
        except PromoCode.DoesNotExist:
            return Response({'error': 'Promo code not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'])
    def checkout(self, request):
        """Checkout cart and create order"""
        cart = self.get_object()
        cart_items = cart.get_items()
        
        if not cart_items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create order
        order_data = {
            'total_amount': cart.get_total(),
            'shipping_address': request.data.get('shipping_address', ''),
            'phone_number': request.data.get('phone_number', ''),
        }
        
        order_serializer = OrderSerializer(data=order_data, context={'request': request})
        if order_serializer.is_valid():
            order = order_serializer.save()
            
            # Create order items
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product_name=item.product_name or (item.product.name if item.product else 'Custom Design'),
                    quantity=item.quantity,
                    price=item.price,
                    custom_design=item.custom_design
                )
            
            # Clear cart
            cart_items.delete()
            cart.promo_code = None
            cart.save()
            
            return Response({
                'message': 'Order created successfully',
                'order': OrderSerializer(order).data
            }, status=status.HTTP_201_CREATED)
        
        return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product', 'custom_design']

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def update_quantity(self, request, pk=None):
        """Update cart item quantity"""
        cart_item = self.get_object()
        quantity = request.data.get('quantity', 1)
        
        if quantity <= 0:
            cart_item.delete()
            return Response({'message': 'Item removed from cart'})
        
        cart_item.quantity = quantity
        cart_item.save()
        
        serializer = self.get_serializer(cart_item)
        return Response(serializer.data)
