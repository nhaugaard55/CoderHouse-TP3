from urllib.parse import quote_plus

from django.conf import settings
from django.db import models


def avatar_upload_to(instance, filename):
    return f"perfiles/{instance.user.username}/{filename}"


class Perfil(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="perfil",
    )
    avatar = models.ImageField(upload_to=avatar_upload_to, blank=True, null=True)
    bio = models.TextField(blank=True)
    sitio_web = models.URLField(blank=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "perfil"
        verbose_name_plural = "perfiles"

    def __str__(self) -> str:
        return f"Perfil de {self.user.get_username()}"

    @property
    def nombre_completo(self):
        nombre = self.user.first_name
        apellido = self.user.last_name
        if nombre or apellido:
            return f"{nombre} {apellido}".strip()
        return self.user.get_username()

    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        nombre = self.user.get_full_name() or self.user.get_username()
        return "https://ui-avatars.com/api/?background=262b33&color=f8f9fa&name=" + quote_plus(nombre)
