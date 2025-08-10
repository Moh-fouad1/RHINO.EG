from django.urls import path
from . import views

urlpatterns = [
    path("contact/", views.shop_contact, name="shop_contact"),
    path('search/', views.shop_search, name='shop_search'),
    path('', views.shop_home, name='shop_home'),
    path('cart/', views.cart_view, name='cart_view'),
    path('upload-design/', views.upload_custom_design, name='upload_custom_design'),
    path('design-success/', views.custom_design_success, name='custom_design_success'),
    path('signup/', views.signup, name='signup'),
]
