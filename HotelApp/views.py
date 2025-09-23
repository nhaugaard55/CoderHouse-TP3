from django.db.models import Q
from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import HabitacionForm, ReservaForm, ServicioForm
from .models import Habitacion, Reserva, Servicio


def home(request):
    return render(request, "home.html")


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


def crear_servicio(request):
    if request.method == "POST":
        form = ServicioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Servicio cargado correctamente.")
            return redirect("lista_reservas")
    else:
        form = ServicioForm()

    return render(request, "formulario.html", {
        "form": form,
        "titulo": "Nuevo servicio",
        "boton": "Guardar servicio",
    })


def lista_reservas(request):
    reservas = Reserva.objects.select_related(
        "habitacion").order_by("check_in")
    return render(request, "lista_reservas.html", {"reservas": reservas})


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
