from django import forms
from .models import CustomDesign

class CustomDesignForm(forms.ModelForm):
    class Meta:
        model = CustomDesign
        fields = ['title', 'description', 'design_file', 'size', 'phone_number']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
