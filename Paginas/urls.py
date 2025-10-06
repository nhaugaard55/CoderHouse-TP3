from django.urls import path

from .views import AboutView, PaginaListView, PaginaDetailView

app_name = "paginas"

urlpatterns = [
    path("about/", AboutView.as_view(), name="about"),
    path("pages/", PaginaListView.as_view(), name="lista"),
    path("pages/<slug:slug>/", PaginaDetailView.as_view(), name="detalle"),
]
