from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Producto
from threading import local

_user = local()  # Variable para manejar usuarios actuales en un entorno multi-hilo

def get_current_user():
    return getattr(_user, 'value', None)

@receiver(pre_save, sender=Producto)
def set_audit_fields_producto(sender, instance, **kwargs):
    user = get_current_user()
    if user and not instance.pk:  # Si es un nuevo registro
        instance.created_by = user
    elif user:  # Si se está actualizando
        instance.updated_by = user
