from django.views.generic import TemplateView, ListView, DetailView

from .models import Pagina

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
