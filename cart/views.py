from django.shortcuts import render, redirect, get_object_or_404
from .models import CartItem, Cart
from shop.models import Product, CustomDesign, PromoCode
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
import json

@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Handle promo code application
    if request.method == 'POST':
        promo_code = request.POST.get('promo_code')
        if promo_code:
            try:
                promo = PromoCode.objects.get(code=promo_code.upper())
                if promo.is_valid():
                    cart.promo_code = promo
                    cart.save()
                    messages.success(request, f"Promo code '{promo.code}' applied! {promo.description}")
                else:
                    messages.error(request, "This promo code is not valid or has expired.")
            except PromoCode.DoesNotExist:
                messages.error(request, "Invalid promo code.")
        else:
            # Remove promo code
            cart.promo_code = None
            cart.save()
            messages.success(request, "Promo code removed.")
    
    subtotal = cart.get_subtotal()
    discount = cart.get_discount()
    total = cart.get_total()
    
    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'discount': discount,
        'total': total,
        'promo_code': cart.promo_code,
        'item_count': cart.get_item_count(),
    }
    return render(request, 'cart/cart.html', context)

@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id, is_active=True)
        quantity = int(request.POST.get('quantity', 1))

        # Check if item already exists in cart
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={
                'product_name': product.name,
                'price': product.base_price,
                'quantity': quantity
            }
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        messages.success(request, f"{product.name} added to cart!")
        return redirect('cart_view')

    return redirect('shop_home')

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    messages.success(request, "Item removed from cart!")
    return redirect('cart_view')

@login_required
def update_cart_quantity(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(CartItem, id=item_id, user=request.user)
        new_quantity = int(request.POST.get('quantity', 1))
        if new_quantity > 0:
            item.quantity = new_quantity
            item.save()
            messages.success(request, "Cart updated!")
        else:
            item.delete()
            messages.success(request, "Item removed from cart!")
    return redirect('cart_view')

@login_required
def apply_promo_code(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        promo_code = data.get('promo_code', '').strip()
        
        if not promo_code:
            return JsonResponse({'success': False, 'error': 'Please enter a promo code.'})
        
        try:
            promo = PromoCode.objects.get(code=promo_code.upper())
            if promo.is_valid():
                cart, created = Cart.objects.get_or_create(user=request.user)
                cart.promo_code = promo
                cart.save()
                
                subtotal = cart.get_subtotal()
                discount = cart.get_discount()
                total = cart.get_total()
                
                return JsonResponse({
                    'success': True,
                    'message': f"Promo code applied! {promo.description}",
                    'subtotal': float(subtotal),
                    'discount': float(discount),
                    'total': float(total),
                    'promo_code': promo.code
                })
            else:
                return JsonResponse({'success': False, 'error': 'This promo code is not valid or has expired.'})
        except PromoCode.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Invalid promo code.'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request.'})

@login_required
def remove_promo_code(request):
    if request.method == 'POST':
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart.promo_code = None
        cart.save()
        
        subtotal = cart.get_subtotal()
        discount = cart.get_discount()
        total = cart.get_total()
        
        return JsonResponse({
            'success': True,
            'message': 'Promo code removed.',
            'subtotal': float(subtotal),
            'discount': float(discount),
            'total': float(total)
        })
    
    return JsonResponse({'success': False, 'error': 'Invalid request.'})
