"""
Modelos base abstractos para toda la aplicación.

Estos modelos proporcionan funcionalidad compartida que otros modelos pueden heredar.
"""

from django.db import models
from django.utils import timezone


class TimestampedModel(models.Model):
    """
    Modelo base abstracto que añade timestamps automáticos.

    Proporciona campos created_at y updated_at que se gestionan automáticamente.
    """

    created_at = models.DateTimeField(
        default=timezone.now,
        db_index=True,
        verbose_name="Fecha de creación",
        help_text="Fecha y hora de creación del registro",
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Fecha de actualización", help_text="Última modificación"
    )

    class Meta:
        abstract = True


class SoftDeletableModel(TimestampedModel):
    """
    Modelo base abstracto que añade soft delete.

    Los registros no se eliminan físicamente, solo se marcan como eliminados.
    Útil para auditoría y trazabilidad.
    """

    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha de eliminación",
        help_text="Fecha y hora de eliminación lógica (soft delete)",
    )

    class Meta:
        abstract = True

    def soft_delete(self) -> None:
        """Marca el registro como eliminado sin borrarlo físicamente."""
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at"])

    def restore(self) -> None:
        """Restaura un registro previamente eliminado."""
        self.deleted_at = None
        self.save(update_fields=["deleted_at"])

    @property
    def is_deleted(self) -> bool:
        """Retorna True si el registro está eliminado (soft delete)."""
        return self.deleted_at is not None
