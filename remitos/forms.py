from django import forms
from .models import Remito, DetalleRemito

class RemitoForm(forms.ModelForm):
    class Meta:
        model = Remito
        fields = ['tipo_remito', 'cliente', 'dep_origen', 'dep_destino', 'nro_comprobante_asoc']
        widgets = {
            'tipo_remito': forms.Select(attrs={'class': 'form-control', 'id': 'id_tipo_remito'}),
            'cliente': forms.Select(attrs={'class': 'form-control', 'id': 'id_cliente'}),
            'dep_origen': forms.Select(attrs={'class': 'form-control', 'id': 'id_dep_origen'}),
            'dep_destino': forms.Select(attrs={'class': 'form-control', 'id': 'id_dep_destino'}),
            'nro_comprobante_asoc': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        tipo_remito = cleaned_data.get('tipo_remito')
        cliente = cleaned_data.get('cliente')
        dep_origen = cleaned_data.get('dep_origen')
        dep_destino = cleaned_data.get('dep_destino')

        # Validaciones específicas para cada tipo de remito
        if tipo_remito == 'compra' and not cliente:
            self.add_error('cliente', 'El cliente es obligatorio para remitos de compra.')
        if tipo_remito == 'venta' and not cliente:
            self.add_error('cliente', 'El cliente es obligatorio para remitos de venta.')
        if tipo_remito == 'interdeposito' and (not dep_origen or not dep_destino):
            self.add_error('dep_origen', 'El depósito origen es obligatorio para remitos de interdepósito.')
            self.add_error('dep_destino', 'El depósito destino es obligatorio para remitos de interdepósito.')

        return cleaned_data


class DetalleRemitoForm(forms.ModelForm):
    class Meta:
        model = DetalleRemito
        fields = ['producto', 'cantidad', 'precio_unit']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control', 'id': 'id_producto'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio_unit': forms.NumberInput(attrs={'class': 'form-control'}),
        }
