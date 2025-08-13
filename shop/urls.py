from django.urls import path
from . import views

urlpatterns = [
    path("", views.shop_home, name="shop_home"),
    path("products/", views.product_list, name="product_list"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),
    path("contact/", views.shop_contact, name="shop_contact"),
    path('search/', views.shop_search, name='shop_search'),

    path('upload-design/', views.upload_custom_design, name='upload_custom_design'),
    path('design-success/', views.custom_design_success, name='custom_design_success'),
    path('signup/', views.signup, name='signup'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('add-review/<int:product_id>/', views.add_review, name='add_review'),
]
