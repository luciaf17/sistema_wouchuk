from django import forms
from django.http import JsonResponse
from django.urls import reverse_lazy
from .models import Producto, Marca, Unidad, Sinonimo, IDTipo1, IDTipo2, DesConcatenada

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

class BaseForm(forms.ModelForm):
    def clean_descripcion(self):
        descripcion = self.cleaned_data['descripcion']
        model = self.Meta.model
        
        # Excluir la instancia actual al validar unicidad
        queryset = model.objects.filter(descripcion=descripcion)
        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)
        
        if queryset.exists():
            raise forms.ValidationError(f"Ya existe un registro con la descripción '{descripcion}'.")
        return descripcion

class MarcaForm(BaseForm):
    class Meta:
        model = Marca
        fields = ['descripcion']
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la descripción de la marca'}),
        }

class UnidadForm(forms.ModelForm):
    class Meta:
        model = Unidad
        fields = ['descripcion', 'abreviatura']  # Include abreviatura
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'abreviatura': forms.TextInput(attrs={'class': 'form-control'}),
        }

class SinonimoForm(BaseForm):
    class Meta:
        model = Sinonimo
        fields = ['descripcion']
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el sinónimo'}),
        }

class IDTipo1Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Cargar atributos, prefijos y sufijos en caso de edición
            self.fields['atributo1'].initial = self.instance.atributo1
            self.fields['atributo2'].initial = self.instance.atributo2
            self.fields['atributo3'].initial = self.instance.atributo3
            self.fields['atributo4'].initial = self.instance.atributo4
            self.fields['atributo5'].initial = self.instance.atributo5
            self.fields['pre1'].initial = self.instance.pre1
            self.fields['pre2'].initial = self.instance.pre2
            self.fields['pre3'].initial = self.instance.pre3
            self.fields['pre4'].initial = self.instance.pre4
            self.fields['pre5'].initial = self.instance.pre5
            self.fields['suf1'].initial = self.instance.suf1
            self.fields['suf2'].initial = self.instance.suf2
            self.fields['suf3'].initial = self.instance.suf3
            self.fields['suf4'].initial = self.instance.suf4
            self.fields['suf5'].initial = self.instance.suf5
            # Si se está editando, carga los sinónimos existentes
            sinonimos = Sinonimo.objects.filter(idtipo1=self.instance).values_list('descripcion', flat=True)
            self.fields['sinonimos'].initial = ', '.join(sinonimos)
    sinonimos = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Escribe o selecciona sinónimos existentes separados por comas',
            'data-autocomplete-url': reverse_lazy('sinonimo_autocomplete')
        }),
        label="Sinónimos"
    )

    class Meta:
        model = IDTipo1
        fields = [
            'descripcion', 'IDtipo2', 'atributo1', 'atributo2', 'atributo3', 
            'atributo4', 'atributo5', 'pre1', 'pre2', 'pre3', 'pre4', 'pre5',
            'suf1', 'suf2', 'suf3', 'suf4', 'suf5', 'cod_alpha',
        ]
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'IDtipo2': forms.TextInput(attrs={'class': 'form-control'}),
            'atributo1': forms.TextInput(attrs={'class': 'form-control', 'data-autocomplete-url': reverse_lazy('atributo_autocomplete')}),
            'atributo2': forms.TextInput(attrs={'class': 'form-control', 'data-autocomplete-url': reverse_lazy('atributo_autocomplete')}),
            'atributo3': forms.TextInput(attrs={'class': 'form-control', 'data-autocomplete-url': reverse_lazy('atributo_autocomplete')}),
            'atributo4': forms.TextInput(attrs={'class': 'form-control', 'data-autocomplete-url': reverse_lazy('atributo_autocomplete')}),
            'atributo5': forms.TextInput(attrs={'class': 'form-control', 'data-autocomplete-url': reverse_lazy('atributo_autocomplete')}),
            'pre1': forms.TextInput(attrs={'class': 'form-control'}),
            'pre2': forms.TextInput(attrs={'class': 'form-control'}),
            'pre3': forms.TextInput(attrs={'class': 'form-control'}),
            'pre4': forms.TextInput(attrs={'class': 'form-control'}),
            'pre5': forms.TextInput(attrs={'class': 'form-control'}),
            'suf1': forms.TextInput(attrs={'class': 'form-control'}),
            'suf2': forms.TextInput(attrs={'class': 'form-control'}),
            'suf3': forms.TextInput(attrs={'class': 'form-control'}),
            'suf4': forms.TextInput(attrs={'class': 'form-control'}),
            'suf5': forms.TextInput(attrs={'class': 'form-control'}),
            'cod_alpha': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        # Guarda la instancia principal del formulario
        instance = super().save(commit=False)

        # Guarda la instancia antes de procesar los sinónimos
        if commit:
            instance.save()

        # Procesar los sinónimos
        sinonimos_text = self.cleaned_data.get('sinonimos', '')
        sinonimos_list = [s.strip() for s in sinonimos_text.split(',') if s.strip()]
        for sinonimo_desc in sinonimos_list:
            # Crear o asociar sinónimos
            sinonimo, created = Sinonimo.objects.get_or_create(descripcion=sinonimo_desc, idtipo1=instance)

        return instance


class IDTipo2Form(forms.ModelForm):
    class Meta:
        model = IDTipo2
        fields = ['descripcion', 'IDtipo1', 'cod_alpha']
        labels = {
            'descripcion': 'Descripción',
            'IDtipo1': 'Grupo (IDTipo1)',
            'cod_alpha': 'Código Alfanumérico',
        }
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['IDtipo1'].queryset = IDTipo1.objects.all()  # Asegura que muestre todos los grupos disponibles

class DesConcatenadaForm(forms.ModelForm):
    class Meta:
        model = DesConcatenada
        fields = [
            'IDtipo1', 'IDtipo2', 'atributo1', 'atributo2', 'atributo3',
            'atributo4', 'atributo5', 'marca', 'unidad'
        ]
        widgets = {
            'IDtipo1': forms.Select(attrs={'class': 'form-control'}),
            'IDtipo2': forms.Select(attrs={'class': 'form-control'}),
            'atributo1': forms.TextInput(attrs={'class': 'form-control'}),
            'atributo2': forms.TextInput(attrs={'class': 'form-control'}),
            'atributo3': forms.TextInput(attrs={'class': 'form-control'}),
            'atributo4': forms.TextInput(attrs={'class': 'form-control'}),
            'atributo5': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.Select(attrs={'class': 'form-control'}),
            'unidad': forms.Select(attrs={'class': 'form-control'}),
            'cod_alpha': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        producto = kwargs.pop('producto', None)
        super().__init__(*args, **kwargs)

        # Prellenar cod_alpha si ya existe
        if self.instance and self.instance.pk:
            self.fields['cod_alpha'].initial = self.instance.cod_alpha

        # Opcional: Puedes usar 'producto' para personalizar el formulario
        if producto:
            self.fields['IDtipo1'].label = f"Grupo para {producto.descripcion}"

         # Prellenar cod_alpha si ya existe
        if self.instance and self.instance.pk:
            self.fields['cod_alpha'].initial = self.instance.cod_alpha

        # Filtrar dinámicamente los IDTipo2 relacionados al IDTipo1 seleccionado
        if 'IDtipo1' in self.data:
            try:
                idtipo1_id = int(self.data.get('IDtipo1'))
                self.fields['IDtipo2'].queryset = IDTipo2.objects.filter(IDtipo1_id=idtipo1_id)
            except (ValueError, TypeError):
                self.fields['IDtipo2'].queryset = IDTipo2.objects.none()
        elif self.instance.pk:
            self.fields['IDtipo2'].queryset = IDTipo2.objects.filter(IDtipo1=self.instance.IDtipo1)
        else:
            self.fields['IDtipo2'].queryset = IDTipo2.objects.none()

        # Cambiar los labels de los atributos para reflejar los nombres definidos en IDTipo1
        if 'IDtipo1' in self.data:
            try:
                idtipo1 = IDTipo1.objects.get(id=self.data.get('IDtipo1'))
                atributos = [
                    idtipo1.atributo1, idtipo1.atributo2, idtipo1.atributo3,
                    idtipo1.atributo4, idtipo1.atributo5
                ]
                for i, atributo in enumerate(atributos, start=1):
                    if atributo:
                        self.fields[f'atributo{i}'].label = atributo
            except IDTipo1.DoesNotExist:
                pass
        elif self.instance.pk:
            atributos = [
                self.instance.IDtipo1.atributo1, self.instance.IDtipo1.atributo2,
                self.instance.IDtipo1.atributo3, self.instance.IDtipo1.atributo4,
                self.instance.IDtipo1.atributo5
            ]
            for i, atributo in enumerate(atributos, start=1):
                if atributo:
                    self.fields[f'atributo{i}'].label = atributo
