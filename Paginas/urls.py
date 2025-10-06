from django.urls import path

from .views import (
    AboutView,
    PaginaListView,
    PaginaDetailView,
    PaginaCreateView,
    PaginaUpdateView,
    PaginaDeleteView,
)

app_name = "paginas"

urlpatterns = [
    path("about/", AboutView.as_view(), name="about"),
    path("pages/", PaginaListView.as_view(), name="lista"),
    path("pages/nueva/", PaginaCreateView.as_view(), name="crear"),
    path("pages/<slug:slug>/editar/", PaginaUpdateView.as_view(), name="editar"),
    path("pages/<slug:slug>/eliminar/", PaginaDeleteView.as_view(), name="eliminar"),
    path("pages/<slug:slug>/", PaginaDetailView.as_view(), name="detalle"),
]
