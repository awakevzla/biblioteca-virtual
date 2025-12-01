from django.db import models

class Libro(models.Model):
  titulo = models.CharField(max_length=200, null=False)
  autor = models.CharField(max_length=200, null=False)
  fecha_publicacion = models.DateField(null=False)
  en_prestamo = models.BooleanField(default=False)

  def __str__(self):
    return f"{self.titulo} - ({self.autor})"

  class Meta:
    verbose_name_plural = "Libros"