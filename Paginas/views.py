from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
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
