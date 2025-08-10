from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CustomDesignForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Product
from django.shortcuts import render

def shop_home(request):
    products = Product.objects.all()
    return render(request, 'shop/home.html', {'products': products})

def shop_search(request):
    query = request.GET.get("q", "")
    results = Product.objects.filter(name__icontains=query) if query else []
    return render(request, "shop/search_results.html", {"results": results, "query": query})

def shop_contact(request):
    return render(request, "shop/contact.html")

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # log them in after signup
            return redirect('upload_custom_design')  # redirect to upload page
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def cart_view(request):
    return render(request, "shop/cart.html")

@login_required
def upload_custom_design(request):
    if request.method == 'POST':
        form = CustomDesignForm(request.POST, request.FILES)
        if form.is_valid():
            custom_design = form.save(commit=False)
            custom_design.user = request.user
            custom_design.save()
            return redirect('shop_home')
    else:
        form = CustomDesignForm()
    
    return render(request, 'shop/upload_design.html', {'form': form})


def custom_design_success(request):
    return render(request, 'shop/custom_design_success.html')


