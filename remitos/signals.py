from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Remito
from utils.middleware import get_current_user  # Importa el método para obtener el usuario actual

@receiver(pre_save, sender=Remito)
def set_audit_fields_remito(sender, instance, **kwargs):
    """
    Señal para registrar quién creó o modificó un remito.
    """
    user = get_current_user()
    if user and not instance.pk:  # Si es un nuevo registro
        instance.created_by = user
    elif user:  # Si se está actualizando
        instance.updated_by = user
