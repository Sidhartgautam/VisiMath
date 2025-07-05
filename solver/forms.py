from django import forms
from .models import EquationImage

class EquationImageForm(forms.ModelForm):
    class Meta:
        model = EquationImage
        fields = ['image']