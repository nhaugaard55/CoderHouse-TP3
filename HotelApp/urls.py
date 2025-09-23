from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("habitaciones/nueva/", views.crear_habitacion, name="crear_habitacion"),
    path("reservas/nueva/", views.crear_reserva, name="crear_reserva"),
    path("servicios/nuevo/", views.crear_servicio, name="crear_servicio"),
    path("reservas/", views.lista_reservas, name="lista_reservas"),
    path("reservas/buscar/", views.buscar_reserva, name="buscar_reserva"),
]
