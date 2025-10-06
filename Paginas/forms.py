from django import forms

from .models import Pagina


class PaginaForm(forms.ModelForm):
    fecha_publicacion = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
    )

    class Meta:
        model = Pagina
        fields = [
            "titulo",
            "slug",
            "extracto",
            "contenido",
            "imagen_portada",
            "fecha_publicacion",
            "destacada",
        ]
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control"}),
            "slug": forms.TextInput(attrs={"class": "form-control"}),
            "extracto": forms.TextInput(attrs={"class": "form-control"}),
            "contenido": forms.Textarea(attrs={"class": "form-control", "rows": 6}),
            "imagen_portada": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "destacada": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.fields["slug"].help_text:
            self.fields["slug"].help_text = "Usá un identificador sin espacios para la URL (ej: spa-lujo)."
