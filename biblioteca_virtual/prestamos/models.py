from django.db import models
from usuarios.models import Usuario
from libros.models import Libro

class Prestamo(models.Model):
  usuario = models.ForeignKey(to=Usuario, on_delete=models.RESTRICT, related_name='prestamos')
  libro = models.ForeignKey(to=Libro, on_delete=models.RESTRICT, related_name='prestamos')
  fecha_prestamo = models.DateTimeField(null=True)
  fecha_devolucion = models.DateTimeField(null=True)

  class Meta:
    verbose_name_plural = "Prestamos"