from django import forms
from .models import CustomDesign

class CustomDesignForm(forms.ModelForm):
    class Meta:
        model = CustomDesign
        fields = ['size', 'framed', 'design_file', 'phone_number']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
