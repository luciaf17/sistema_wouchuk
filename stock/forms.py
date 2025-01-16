# forms.py
from django import forms
from .models import Deposito, Pasillo, Columna, Estante

class BaseForm(forms.ModelForm):
    def clean_descripcion(self):
        descripcion = self.cleaned_data['descripcion']
        model = self.Meta.model
        if model.objects.filter(descripcion=descripcion).exists():
            raise forms.ValidationError(f"Ya existe un registro con la descripción '{descripcion}'.")
        return descripcion

class DepositoForm(BaseForm):
    class Meta:
        model = Deposito
        fields = ['descripcion', 'ubicacion']
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre del depósito'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la ubicación del depósito'}),
        }


class PasilloForm(BaseForm):
    class Meta:
        model = Pasillo
        fields = ['descripcion']
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ColumnaForm(BaseForm):
    class Meta:
        model = Columna
        fields = ['descripcion']
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
        }


class EstanteForm(BaseForm):
    class Meta:
        model = Estante
        fields = ['descripcion']
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
        }