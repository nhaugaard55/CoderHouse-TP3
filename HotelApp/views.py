from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render
from .forms import HabitacionForm, ReservaForm
from .models import Habitacion, Reserva


@login_required
def home(request):
    return render(request, "home.html")


@login_required
def crear_habitacion(request):
    if request.method == "POST":
        form = HabitacionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Habitación creada correctamente.")
            return redirect("lista_reservas")
    else:
        form = HabitacionForm()

    return render(request, "formulario.html", {
        "form": form,
        "titulo": "Nueva habitación",
        "boton": "Guardar habitación",
    })


@login_required
def crear_reserva(request):
    if request.method == "POST":
        form = ReservaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Reserva creada correctamente.")
            return redirect("lista_reservas")
    else:
        form = ReservaForm()

    return render(request, "formulario.html", {
        "form": form,
        "titulo": "Nueva reserva",
        "boton": "Guardar reserva",
    })


@login_required
def lista_reservas(request):
    reservas = Reserva.objects.select_related(
        "habitacion").order_by("check_in")
    return render(request, "lista_reservas.html", {"reservas": reservas})


@login_required
def buscar_reserva(request):
    query = request.GET.get("q", "").strip()
    resultados = []

    if query:
        resultados = Reserva.objects.select_related("habitacion").filter(
            Q(apellido__icontains=query) | Q(nombre__icontains=query) | Q(
                habitacion__numero__icontains=query)
        ).order_by("check_in")

    return render(request, "buscar_reserva.html", {
        "query": query,
        "resultados": resultados,
    })
