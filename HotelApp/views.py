import calendar
from datetime import date, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render
from django.utils import timezone

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


@login_required
def calendario_reservas(request):
    today = timezone.localdate()
    try:
        month = int(request.GET.get("month", today.month))
        year = int(request.GET.get("year", today.year))
    except ValueError:
        month = today.month
        year = today.year

    first_day = date(year, month, 1)
    last_day_number = calendar.monthrange(year, month)[1]
    last_day = date(year, month, last_day_number)
    total_days = (last_day - first_day).days + 1
    days = [first_day + timedelta(days=i) for i in range(total_days)]

    prev_month_date = first_day - timedelta(days=1)
    next_month_date = last_day + timedelta(days=1)

    habitaciones = Habitacion.objects.order_by("numero")
    reservas = (
        Reserva.objects.select_related("habitacion")
        .filter(check_out__gte=first_day, check_in__lte=last_day)
        .order_by("habitacion__numero", "check_in")
    )

    reservas_por_habitacion = {habitacion.id: {} for habitacion in habitaciones}

    for reserva in reservas:
        inicio = max(reserva.check_in, first_day)
        fin = min(reserva.check_out, last_day)
        actual = inicio
        while actual <= fin:
            reservas_por_habitacion[reserva.habitacion_id][actual] = reserva
            actual += timedelta(days=1)

    filas_calendario = []
    for habitacion in habitaciones:
        celdas = []
        mapa = reservas_por_habitacion.get(habitacion.id, {})
        for dia in days:
            celdas.append({
                "dia": dia,
                "reserva": mapa.get(dia),
            })
        filas_calendario.append({
            "habitacion": habitacion,
            "celdas": celdas,
        })

    contexto = {
        "dias": days,
        "filas_calendario": filas_calendario,
        "today": today,
        "current_month": month,
        "current_year": year,
        "month_name": calendar.month_name[month],
        "prev_month": prev_month_date.month,
        "prev_year": prev_month_date.year,
        "next_month": next_month_date.month,
        "next_year": next_month_date.year,
        "weekday_names": [calendar.day_abbr[d.weekday()] for d in days],
    }

    return render(request, "reservas_calendario.html", contexto)
