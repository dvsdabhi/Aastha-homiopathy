from django import forms
from aastha.models import Treatment, TreatmentCategory

class TreatmentForm(forms.ModelForm):
    class Meta:
        model = Treatment
        fields = ['category', 'title', 'description', 'image']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = TreatmentCategory
        fields = ['name']
