from django.shortcuts import render
from django.views.generic import TemplateView


class homeweb(TemplateView):
    template_name = "home/index.html"

    def get(self, request):
        return render(request, 'home/index.html', {})
