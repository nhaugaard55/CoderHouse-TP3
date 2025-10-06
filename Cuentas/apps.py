from django.apps import AppConfig


class CuentasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Cuentas'

    def ready(self) -> None:
        from . import signals  # noqa: F401

        return super().ready()
