from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from .forms import CustomDesignForm, ReviewForm, OrderForm, ContactForm
from .forms import CustomSignUpForm
from django.contrib.auth import login
from .models import Product, CustomDesign, Review, Order, OrderItem, Category
from cart.models import CartItem, Cart

def shop_home(request):
    featured_products = Product.objects.filter(featured=True, is_active=True)[:8]
    categories = Category.objects.filter(is_active=True)[:6]
    latest_products = Product.objects.filter(is_active=True)[:4]
    
    context = {
        'featured_products': featured_products,
        'categories': categories,
        'latest_products': latest_products,
    }
    return render(request, 'shop/home.html', context)

def product_list(request):
    products = Product.objects.filter(is_active=True)
    category = request.GET.get('category')
    search = request.GET.get('search')
    
    if category:
        products = products.filter(category__slug=category)
    
    if search:
        products = products.filter(
            Q(name__icontains=search) | 
            Q(description__icontains=search) |
            Q(category__name__icontains=search)
        )
    
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.filter(is_active=True)
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'current_category': category,
        'search': search,
    }
    return render(request, 'shop/product_list.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = Product.objects.filter(category=product.category, is_active=True).exclude(id=product.id)[:4]
    reviews = Review.objects.filter(product=product, is_approved=True)[:5]
    
    if request.method == 'POST' and request.user.is_authenticated:
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, 'Review submitted successfully!')
            return redirect('product_detail', slug=slug)
    else:
        review_form = ReviewForm()
    
    context = {
        'product': product,
        'related_products': related_products,
        'reviews': reviews,
        'review_form': review_form,
    }
    return render(request, 'shop/product_detail.html', context)

def shop_search(request):
    query = request.GET.get("q", "")
    if query:
        results = Product.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(category__name__icontains=query),
            is_active=True
        )
    else:
        results = []
    
    context = {
        "results": results, 
        "query": query
    }
    return render(request, "shop/search_results.html", context)

def shop_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('shop_contact')
    else:
        form = ContactForm()
    
    return render(request, "shop/contact.html", {'form': form})

def signup(request):
    if request.method == 'POST':
        form = CustomSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully! Welcome to RHINO.EG!")
            return redirect('upload_custom_design')
    else:
        form = CustomSignUpForm()
    return render(request, 'registration/signup.html', {'form': form})



@login_required
def upload_custom_design(request):
    if request.method == 'POST':
        form = CustomDesignForm(request.POST, request.FILES)
        if form.is_valid():
            custom_design = form.save(commit=False)
            custom_design.user = request.user
            custom_design.save()
            custom_design.add_to_cart()
            messages.success(request, f"Your custom design has been added to cart! Total: {custom_design.calculate_price()} LE")
            return redirect('cart_view')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomDesignForm()
    
    return render(request, 'shop/upload_design.html', {'form': form})

def custom_design_success(request):
    return render(request, 'shop/custom_design_success.html')

@login_required
def add_review(request, product_id):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product_id = product_id
            review.save()
            messages.success(request, "Thank you for your review!")
            return redirect('shop_home')
    return redirect('shop_home')

@login_required
def checkout(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            cart_items = CartItem.objects.filter(user=request.user)
            if not cart_items.exists():
                messages.error(request, "Your cart is empty!")
                return redirect('cart_view')
            
            # Get cart with promo code
            cart, created = Cart.objects.get_or_create(user=request.user)
            total_amount = cart.get_total()
            
            order = form.save(commit=False)
            order.user = request.user
            order.total_amount = total_amount
            order.save()
            
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product_name=cart_item.product_name,
                    quantity=cart_item.quantity,
                    price=cart_item.price,
                    custom_design=cart_item.custom_design
                )
            
            # Clear cart and promo code
            cart_items.delete()
            cart.promo_code = None
            cart.save()
            
            messages.success(request, f"Order placed successfully! Order number: {order.order_number}")
            return redirect('order_detail', order_id=order.id)
    else:
        form = OrderForm()
    
    # Get cart with promo code
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.get_items()
    subtotal = cart.get_subtotal()
    discount = cart.get_discount()
    total = cart.get_total()
    
    context = {
        'form': form,
        'cart_items': cart_items,
        'subtotal': subtotal,
        'discount': discount,
        'total': total,
        'promo_code': cart.promo_code,
    }
    return render(request, 'shop/checkout.html', context)

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'shop/order_detail.html', {'order': order})

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'shop/my_orders.html', {'orders': orders})




