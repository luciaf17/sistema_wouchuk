from django.db import models
from django.contrib.auth.models import User

class AuditModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación
    updated_at = models.DateTimeField(auto_now=True)  # Fecha de última modificación
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_%(class)s")
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="updated_%(class)s")

    class Meta:
        abstract = True  # Modelo abstracto (no crea tabla en la base de datos)
