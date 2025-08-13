from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CustomDesign, Review, Order, OrderItem

class CustomSignUpForm(UserCreationForm):
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={
        'class': 'auth-input',
        'placeholder': 'Email (optional)'
    }))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'auth-input',
            'placeholder': 'Username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'auth-input',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'auth-input',
            'placeholder': 'Confirm Password'
        })

class CustomDesignForm(forms.ModelForm):
    class Meta:
        model = CustomDesign
        fields = ['framed', 'size', 'design_file', 'phone_number', 'notes']
        widgets = {
            'framed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'size': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'design_file': forms.FileInput(attrs={'class': 'form-control d-none', 'accept': 'image/*'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter your phone number'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any special instructions or notes...'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Share your experience with this product...'}),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['shipping_address', 'phone_number']
        widgets = {
            'shipping_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter your shipping address...'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
        }

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}))
    subject = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Your Message'}))
