from django.views.generic import TemplateView


class AboutView(TemplateView):
    template_name = "paginas/about.html"
