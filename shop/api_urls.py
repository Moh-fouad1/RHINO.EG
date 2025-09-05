from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .api_views import (
    RegisterView, CategoryViewSet, ProductViewSet, CustomDesignViewSet,
    ReviewViewSet, OrderViewSet, PromoCodeViewSet, CartViewSet, CartItemViewSet
)

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'custom-designs', CustomDesignViewSet, basename='customdesign')
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'promo-codes', PromoCodeViewSet)
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'cart-items', CartItemViewSet, basename='cartitem')

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', RegisterView.as_view(), name='api_register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='api_login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='api_refresh'),
    path('auth/verify/', TokenVerifyView.as_view(), name='api_verify'),
    
    # API endpoints
    path('', include(router.urls)),
]
