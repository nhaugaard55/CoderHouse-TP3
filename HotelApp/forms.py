from django import forms
from .models import Habitacion, Reserva, Servicio


class BootstrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs.setdefault("class", "form-check-input")
            else:
                existing = widget.attrs.get("class", "")
                widget.attrs["class"] = (existing + " form-control").strip()


class HabitacionForm(BootstrapModelForm):
    class Meta:
        model = Habitacion
        fields = "__all__"


class ReservaForm(BootstrapModelForm):
    class Meta:
        model = Reserva
        fields = "__all__"
        widgets = {
            "check_in": forms.DateInput(attrs={"type": "date"}),
            "check_out": forms.DateInput(attrs={"type": "date"}),
        }


class ServicioForm(BootstrapModelForm):
    class Meta:
        model = Servicio
        fields = "__all__"
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date"}),
        }
