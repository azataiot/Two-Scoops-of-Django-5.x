# tastings/views.py

from django.views.generic import ListView, DetailView, UpdateView
from .models import Tasting
from django.urls import reverse
# Example 10.1: Using Mixins in a View
from django.views.generic import TemplateView


class TasteListView(ListView):
    model = Tasting


class TasteDetailView(DetailView):
    model = Tasting


class TasteResultsView(ListView):
    template_name = 'tastings/results.html'


class TasteUpdateView(UpdateView):
    model = Tasting

    def get_success_url(self):
        return reverse('tastings:detail',
                       kwargs={
                           'pk': self.object.pk,
                       })


# Example 10.1: Using Mixins in a View

class FreshFruitMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["has_fresh_fruit"] = True
        return context


class FruityFlavorView(FreshFruitMixin, TemplateView):
    template_name = "fruity_flavor.html"
