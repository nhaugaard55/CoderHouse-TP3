from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Perfil


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def guardar_perfil_usuario(sender, instance, **kwargs):
    if hasattr(instance, "perfil"):
        instance.perfil.save()
