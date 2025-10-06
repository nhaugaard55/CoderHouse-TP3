from django.contrib import admin

from .models import Perfil


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ("user", "nombre", "email", "actualizado")
    search_fields = ("user__username", "user__first_name", "user__last_name", "user__email")
    list_select_related = ("user",)

    @admin.display(ordering="user__first_name", description="Nombre")
    def nombre(self, obj):
        return obj.user.get_full_name() or obj.user.get_username()

    @admin.display(ordering="user__email", description="Email")
    def email(self, obj):
        return obj.user.email
