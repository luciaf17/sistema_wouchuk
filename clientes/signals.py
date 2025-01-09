from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Cliente, TipoDocumento
from utils.middleware import get_current_user  # Importa la función del middleware para obtener el usuario actual

# Señal para el modelo Cliente
@receiver(pre_save, sender=Cliente)
def set_audit_fields_cliente(sender, instance, **kwargs):
    user = get_current_user()
    if user:
        if not instance.pk:  # Si es un nuevo registro
            instance.created_by = user
        else:  # Si se está actualizando
            instance.updated_by = user

# Señal para el modelo TipoDocumento
@receiver(pre_save, sender=TipoDocumento)
def set_audit_fields_tipodocumento(sender, instance, **kwargs):
    user = get_current_user()
    if user:
        if not instance.pk:  # Si es un nuevo registro
            instance.created_by = user
        else:  # Si se está actualizando
            instance.updated_by = user
