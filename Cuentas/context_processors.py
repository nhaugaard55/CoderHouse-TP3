from .models import Perfil


def perfil_actual(request):
    if not request.user.is_authenticated:
        return {}

    perfil, _ = Perfil.objects.get_or_create(user=request.user)
    return {"perfil_actual": perfil}
