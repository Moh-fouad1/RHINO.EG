#!/usr/bin/env python
import os
import sys
import django
from datetime import datetime, timedelta

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rhino_eg.settings')
django.setup()

from shop.models import Category, Product, PromoCode
from django.utils.text import slugify

def create_sample_data():
    # Create categories
    categories = [
        {'name': 'Abstract Art', 'description': 'Modern abstract designs'},
        {'name': 'Nature', 'description': 'Beautiful nature scenes'},
        {'name': 'Minimalist', 'description': 'Clean and simple designs'},
        {'name': 'Vintage', 'description': 'Classic vintage designs'},
        {'name': 'Modern', 'description': 'Contemporary modern designs'},
        {'name': 'Artistic', 'description': 'Creative artistic designs'},
    ]
    
    for cat_data in categories:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={
                'description': cat_data['description'],
                'slug': slugify(cat_data['name']),
                'is_active': True
            }
        )
        print(f"{'Created' if created else 'Found'} category: {category.name}")
    
    # Create sample promo codes
    promo_codes = [
        {
            'code': 'WELCOME10',
            'description': '10% off for new customers',
            'discount_type': 'percentage',
            'discount_value': 10.00,
            'min_order_amount': 50.00,
            'max_uses': 100,
            'valid_from': datetime.now(),
            'valid_until': datetime.now() + timedelta(days=30),
        },
        {
            'code': 'SAVE20',
            'description': '20% off on orders over $100',
            'discount_type': 'percentage',
            'discount_value': 20.00,
            'min_order_amount': 100.00,
            'max_uses': 50,
            'valid_from': datetime.now(),
            'valid_until': datetime.now() + timedelta(days=60),
        },
        {
            'code': 'FREESHIP',
            'description': 'Free shipping on any order',
            'discount_type': 'fixed',
            'discount_value': 15.00,
            'min_order_amount': 0.00,
            'max_uses': 200,
            'valid_from': datetime.now(),
            'valid_until': datetime.now() + timedelta(days=90),
        },
        {
            'code': 'FLASH25',
            'description': '25% off flash sale',
            'discount_type': 'percentage',
            'discount_value': 25.00,
            'min_order_amount': 75.00,
            'max_uses': 25,
            'valid_from': datetime.now(),
            'valid_until': datetime.now() + timedelta(days=7),
        },
    ]
    
    for promo_data in promo_codes:
        promo, created = PromoCode.objects.get_or_create(
            code=promo_data['code'],
            defaults=promo_data
        )
        print(f"{'Created' if created else 'Found'} promo code: {promo.code}")
    
    # Create sample products
    products = [
        {
            'name': 'Abstract Blue Waves',
            'description': 'Beautiful abstract design with flowing blue waves',
            'base_price': 30.00,
            'size': 'A4',
            'framed': False,
            'featured': True,
            'in_stock': True,
            'is_active': True,
            'category': Category.objects.get(name='Abstract Art'),
        },
        {
            'name': 'Mountain Landscape',
            'description': 'Stunning mountain landscape with sunset colors',
            'base_price': 35.00,
            'size': 'A3',
            'framed': True,
            'featured': True,
            'in_stock': True,
            'is_active': True,
            'category': Category.objects.get(name='Nature'),
        },
        {
            'name': 'Minimalist Geometric',
            'description': 'Clean geometric patterns in black and white',
            'base_price': 25.00,
            'size': 'A5',
            'framed': False,
            'featured': True,
            'in_stock': True,
            'is_active': True,
            'category': Category.objects.get(name='Minimalist'),
        },
        {
            'name': 'Floral Pattern',
            'description': 'Elegant floral design with vibrant colors',
            'base_price': 30.00,
            'size': 'A4',
            'framed': True,
            'featured': True,
            'in_stock': True,
            'is_active': True,
            'category': Category.objects.get(name='Artistic'),
        },
        {
            'name': 'Vintage Retro',
            'description': 'Classic vintage design with retro elements',
            'base_price': 35.00,
            'size': 'A3',
            'framed': False,
            'featured': True,
            'in_stock': True,
            'is_active': True,
            'category': Category.objects.get(name='Vintage'),
        },
        {
            'name': 'Modern Lines',
            'description': 'Contemporary design with clean lines',
            'base_price': 30.00,
            'size': 'A4',
            'framed': True,
            'featured': True,
            'in_stock': True,
            'is_active': True,
            'category': Category.objects.get(name='Modern'),
        },
    ]
    
    for prod_data in products:
        product, created = Product.objects.get_or_create(
            name=prod_data['name'],
            defaults={
                **prod_data,
                'slug': slugify(prod_data['name']),
            }
        )
        print(f"{'Created' if created else 'Found'} product: {product.name} - {product.get_final_price()} LE")

if __name__ == '__main__':
    print("Creating sample data for RHINO.EG...")
    create_sample_data()
    print("Sample data creation completed!")
