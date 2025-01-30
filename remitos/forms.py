from django import forms
from .models import Remito, DetalleRemito, ConversionMoneda

class RemitoForm(forms.ModelForm):
    class Meta:
        model = Remito
        fields = ['tipo_remito', 'cliente', 'nro_comprobante_asoc']
        widgets = {
            'tipo_remito': forms.Select(attrs={'class': 'form-control', 'id': 'id_tipo_remito'}),
            'cliente': forms.Select(attrs={'class': 'form-control', 'id': 'id_cliente'}),
            'nro_comprobante_asoc': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        tipo_remito = cleaned_data.get('tipo_remito')
        cliente = cleaned_data.get('cliente')

        # Validaciones específicas para cada tipo de remito
        if tipo_remito in ['compra', 'venta'] and not cliente:
            self.add_error('cliente', 'El cliente es obligatorio para remitos de compra o venta.')

        return cleaned_data



class DetalleRemitoForm(forms.ModelForm):
    class Meta:
        model = DetalleRemito
        fields = ['producto', 'dep_origen', 'dep_destino', 'cantidad', 'moneda', 'precio_unit']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control', 'id': 'id_producto'}),
            'dep_origen': forms.Select(attrs={'class': 'form-control', 'id': 'id_dep_origen'}),
            'dep_destino': forms.Select(attrs={'class': 'form-control', 'id': 'id_dep_destino'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio_unit': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class ConversionMonedaForm(forms.ModelForm):
    class Meta:
        model = ConversionMoneda
        fields = ['moneda', 'simbolo', 'conversion']
        widgets = {
            'moneda': forms.TextInput(attrs={'class': 'form-control'}),
            'simbolo': forms.TextInput(attrs={'class': 'form-control'}),
            'conversion': forms.NumberInput(attrs={'class': 'form-control'}),
        }