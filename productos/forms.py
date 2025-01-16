from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['barcode', 'descripcion', 'loc_dep', 'loc_pas', 'loc_col', 'loc_est']
        widgets = {
            'barcode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escanea el código de barras'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'loc_dep': forms.Select(attrs={'class': 'form-control'}),
            'loc_pas': forms.Select(attrs={'class': 'form-control'}),
            'loc_col': forms.Select(attrs={'class': 'form-control'}),
            'loc_est': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_barcode(self):
        barcode = self.cleaned_data.get('barcode')
        if barcode:
            # Verificar si ya existe un producto con el mismo barcode, excluyendo el actual si se está editando
            queryset = Producto.objects.filter(barcode=barcode)
            if self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.exists():
                raise forms.ValidationError("El código de barras ya existe.")
        return barcode

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion')
        if descripcion:
            # Verificar si ya existe un producto con la misma descripción, excluyendo el actual si se está editando
            queryset = Producto.objects.filter(descripcion=descripcion)
            if self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.exists():
                raise forms.ValidationError("La descripción ya existe.")
        return descripcion

