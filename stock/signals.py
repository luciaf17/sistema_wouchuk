from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Stock
from utils.middleware import get_current_user  # Importa el método para obtener el usuario actual

@receiver(pre_save, sender=Stock)
def set_audit_fields_stock(sender, instance, **kwargs):
    """
    Señal para registrar quién creó o modificó el stock.
    """
    user = get_current_user()
    if user and not instance.pk:  # Si es un nuevo registro
        instance.created_by = user
    elif user:  # Si se está actualizando
        instance.updated_by = user
