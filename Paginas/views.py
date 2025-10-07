from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import Pagina
from .forms import PaginaForm


def completar_campos_automaticos(pagina: Pagina) -> None:
    base_slug = slugify(pagina.titulo) or "novedad"
    slug = base_slug
    qs = Pagina.objects.all()
    if pagina.pk:
        qs = qs.exclude(pk=pagina.pk)
    contador = 1
    while qs.filter(slug=slug).exists():
        slug = f"{base_slug}-{contador}"
        contador += 1
    pagina.slug = slug
    contenido = (pagina.contenido or "").strip()
    pagina.extracto = contenido[:200]

class AboutView(TemplateView):
    template_name = "paginas/about.html"


class PaginaListView(ListView):
    model = Pagina
    template_name = "paginas/pagina_list.html"
    context_object_name = "paginas"
    paginate_by = 6


class PaginaDetailView(DetailView):
    model = Pagina
    template_name = "paginas/pagina_detail.html"
    context_object_name = "pagina"
    slug_field = "slug"
    slug_url_kwarg = "slug"


class PaginaCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = PaginaForm
    template_name = "paginas/pagina_form.html"
    success_message = "Novedad creada correctamente."
    success_url = reverse_lazy("paginas:lista")

    def form_valid(self, form):
        form.instance.autor = self.request.user
        completar_campos_automaticos(form.instance)
        return super().form_valid(form)


class AutorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        pagina = self.get_object()
        if pagina.autor_id is None:
            return self.request.user.is_staff
        return pagina.autor_id == self.request.user.id or self.request.user.is_staff

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect_to_login(self.request.get_full_path())
        raise PermissionDenied


class PaginaUpdateView(AutorRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Pagina
    form_class = PaginaForm
    template_name = "paginas/pagina_form.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    success_message = "Novedad actualizada correctamente."
    success_url = reverse_lazy("paginas:lista")

    def form_valid(self, form):
        completar_campos_automaticos(form.instance)
        return super().form_valid(form)


class PaginaDeleteView(AutorRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Pagina
    template_name = "paginas/pagina_confirm_delete.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    success_url = reverse_lazy("paginas:lista")

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, "Novedad eliminada correctamente.")
        return response
