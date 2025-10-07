from django.urls import path

from .views import (
    CambiarPasswordView,
    CustomLoginView,
    CustomLogoutView,
    PerfilView,
    RegistroView,
    editar_perfil,
    eliminar_perfil,
)

app_name = "cuentas"

urlpatterns = [
    path("accounts/login/", CustomLoginView.as_view(), name="login"),
    path("accounts/logout/", CustomLogoutView.as_view(), name="logout"),
    path("accounts/registro/", RegistroView.as_view(), name="registro"),
    path("accounts/perfil/", PerfilView.as_view(), name="perfil"),
    path("accounts/perfil/editar/", editar_perfil, name="editar_perfil"),
    path("accounts/perfil/eliminar/", eliminar_perfil, name="eliminar_perfil"),
    path("accounts/password/cambiar/", CambiarPasswordView.as_view(), name="password_cambiar"),
]
