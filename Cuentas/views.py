from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import PerfilForm, RegistroUsuarioForm, UsuarioUpdateForm
from .models import Perfil


class CustomLoginView(LoginView):
    template_name = "cuentas/login.html"
    redirect_authenticated_user = True

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["username"].widget.attrs.setdefault("class", "form-control")
        form.fields["password"].widget.attrs.setdefault("class", "form-control")
        return form


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("home")


class RegistroView(CreateView):
    template_name = "cuentas/registro.html"
    form_class = RegistroUsuarioForm
    model = User
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, "Tu cuenta se creó correctamente. ¡Bienvenido a The Paradise Hotel!")
        return response


class PerfilView(LoginRequiredMixin, TemplateView):
    template_name = "cuentas/perfil.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        perfil, _ = Perfil.objects.get_or_create(user=self.request.user)
        context["perfil"] = perfil
        return context


@login_required
def editar_perfil(request):
    usuario = request.user
    perfil, _ = Perfil.objects.get_or_create(user=usuario)

    if request.method == "POST":
        usuario_form = UsuarioUpdateForm(request.POST, instance=usuario)
        perfil_form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if usuario_form.is_valid() and perfil_form.is_valid():
            usuario_form.save()
            perfil_form.save()
            messages.success(request, "Perfil actualizado correctamente.")
            return redirect("cuentas:perfil")
    else:
        usuario_form = UsuarioUpdateForm(instance=usuario)
        perfil_form = PerfilForm(instance=perfil)

    return render(request, "cuentas/perfil_form.html", {
        "usuario_form": usuario_form,
        "perfil_form": perfil_form,
    })


class CambiarPasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = "cuentas/password_change.html"
    success_url = reverse_lazy("cuentas:perfil")

    def form_valid(self, form):
        messages.success(self.request, "Tu contraseña se actualizó correctamente.")
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field in form.fields.values():
            field.widget.attrs.setdefault("class", "form-control")
        return form
