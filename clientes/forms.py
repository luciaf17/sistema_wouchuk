from django import forms
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError
from .models import TipoDocumento, CategoriaArca, Rubro, Departamento, TipoCliente, Pais, Provincia, Localidad, Cliente, ClienteTipo, Contacto


#forms tipoDocumento
class TipoDocumentoForm(forms.ModelForm):
    class Meta:
        model = TipoDocumento
        fields = ['descripcion']
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el tipo de documento'}),
        }

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion')
        
        # Normalizamos para la validación (para verificar duplicados)
        descripcion_normalizada = descripcion.strip().lower()
        if TipoDocumento.objects.filter(descripcion__iexact=descripcion_normalizada).exists():
            raise forms.ValidationError(f"El tipo de documento '{descripcion}' ya existe.")
        
        # Devolvemos la descripción tal cual la ingresó el usuario
        return descripcion

#Forms categoriaArca
class CategoriaArcaForm(forms.ModelForm):
    class Meta:
        model = CategoriaArca
        fields = ['descripcion']
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la descripción'}),
        }

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion')
        
        # Normalizamos para la validación (para verificar duplicados)
        descripcion_normalizada = descripcion.strip().lower()
        if CategoriaArca.objects.filter(descripcion__iexact=descripcion_normalizada).exists():
            raise forms.ValidationError(f"La categoría '{descripcion}' ya existe.")
        
        # Devolvemos la descripción tal cual la ingresó el usuario
        return descripcion
    

class RubroForm(forms.ModelForm):
    class Meta:
        model = Rubro
        fields = ['descripcion']
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion')
        # Normalizamos para verificar duplicados
        descripcion_normalizada = descripcion.strip().lower()
        if Rubro.objects.filter(descripcion__iexact=descripcion_normalizada).exists():
            raise forms.ValidationError(f"El rubro '{descripcion}' ya existe.")
        return descripcion
    
class DepartamentoForm(forms.ModelForm):
    class Meta:
        model = Departamento
        fields = ['descripcion']
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion')
        # Normalización para evitar duplicados
        descripcion_normalizada = descripcion.strip().lower()
        if Departamento.objects.filter(descripcion__iexact=descripcion_normalizada).exists():
            raise forms.ValidationError(f"El departamento '{descripcion}' ya existe.")
        return descripcion
    
class TipoClienteForm(forms.ModelForm):
    class Meta:
        model = TipoCliente
        fields = ['descripcion']
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion')
        # Normalización para evitar duplicados
        descripcion_normalizada = descripcion.strip().lower()
        if TipoCliente.objects.filter(descripcion__iexact=descripcion_normalizada).exists():
            raise forms.ValidationError(f"El tipo de cliente '{descripcion}' ya existe.")
        return descripcion
    
class PaisForm(forms.ModelForm):
    class Meta:
        model = Pais
        fields = ['descripcion', 'cod_tel', 'gtm']
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del país'}),
            'cod_tel': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código telefónico'}),
            'gtm': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zona horaria'}),
        }

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion').strip()
        # Excluir el objeto actual en caso de edición
        pais_id = self.instance.pk  # ID del registro actual
        if Pais.objects.filter(descripcion__iexact=descripcion).exclude(pk=pais_id).exists():
            raise forms.ValidationError(f"El país '{descripcion}' ya existe.")
        return descripcion
    
class ProvinciaForm(forms.ModelForm):
    class Meta:
        model = Provincia
        fields = ['descripcion', 'pais']
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la provincia'}),
            'pais': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion').strip()
        pais = self.cleaned_data.get('pais')
        provincia_id = self.instance.pk  # ID del registro actual
        # Validar que no exista otra provincia con el mismo nombre para el mismo país
        if Provincia.objects.filter(descripcion__iexact=descripcion, pais=pais).exclude(pk=provincia_id).exists():
            raise forms.ValidationError(f"La provincia '{descripcion}' ya existe en el país seleccionado.")
        return descripcion
    
class LocalidadForm(forms.ModelForm):
    class Meta:
        model = Localidad
        fields = ['descripcion', 'cp', 'provincia']
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la localidad'}),
            'cp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código postal'}),
            'provincia': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion').strip()
        provincia = self.cleaned_data.get('provincia')
        localidad_id = self.instance.pk  # ID del registro actual
        # Validar duplicados por descripción y provincia
        if Localidad.objects.filter(descripcion__iexact=descripcion, provincia=provincia).exclude(pk=localidad_id).exists():
            raise forms.ValidationError(f"La localidad '{descripcion}' ya existe en la provincia seleccionada.")
        return descripcion
    
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['descripcion', 'fantasia', 'cat_arca', 'tipo_doc', 'nro_doc', 'direccion', 'localidad', 'rubro']
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Razón Social'}),
            'fantasia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre Fantasía'}),
            'cat_arca': forms.Select(attrs={'class': 'form-control'}),
            'tipo_doc': forms.Select(attrs={'class': 'form-control'}),
            'nro_doc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de Documento'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección'}),
            'localidad': forms.Select(attrs={'class': 'form-control'}),
            'rubro': forms.Select(attrs={'class': 'form-control'}),
        }
    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion').strip()
        cliente_id = self.instance.pk  # ID del registro actual
        # Validar duplicados por descripción
        if Cliente.objects.filter(descripcion__iexact=descripcion).exclude(pk=cliente_id).exists():
            raise forms.ValidationError(f"El cliente '{descripcion}' ya existe.")
        return descripcion

class ClienteTipoForm(forms.ModelForm):
    class Meta:
        model = ClienteTipo
        fields = ['tipo_cliente', 'principal']
        widgets = {
            'tipo_cliente': forms.Select(attrs={'class': 'form-control'}),
            'principal': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    def clean(self):
        super().clean()
        principales = [form.cleaned_data.get('principal') for form in self.forms if not form.cleaned_data.get('DELETE')]
        if principales.count(True) > 1:
            raise ValidationError("Solo puede haber un tipo de cliente marcado como principal.")

# Inline formset para ClienteTipo
ClienteTipoFormSet = inlineformset_factory(
    Cliente, ClienteTipo,
    form=ClienteTipoForm,
    extra=1,  # Número de formularios vacíos que se añaden
    can_delete=True
)

class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ['cliente', 'departamento', 'nombre_y_apellido', 'telefono', 'email']
        widgets = {
            'cliente': forms.HiddenInput(),  # El cliente será asignado automáticamente
            'departamento': forms.Select(attrs={'class': 'form-control'}),
            'nombre_y_apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }