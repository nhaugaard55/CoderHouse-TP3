from django.conf import settings
from django.db import models


class Pagina(models.Model):
    titulo = models.CharField(max_length=150)
    slug = models.SlugField(max_length=160, unique=True)
    extracto = models.CharField(max_length=250)
    contenido = models.TextField()
    imagen_portada = models.ImageField(upload_to="paginas/", blank=True)
    fecha_publicacion = models.DateField()
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="paginas",
    )
    destacada = models.BooleanField(default=False)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-fecha_publicacion", "-creado"]
        verbose_name = "página"
        verbose_name_plural = "páginas"

    def __str__(self) -> str:
        return self.titulo

    def get_absolute_url(self):
        return f"/pages/{self.slug}/"
