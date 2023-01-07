from django.urls import reverse_lazy
from django.views import generic

from .models import Shop


class IndexView(generic.ListView):
    model = Shop


class DetailView(generic.DetailView):
    model = Shop


class CreateView(generic.edit.CreateView):
    model = Shop
    fields = "__all__"


class UpdateView(generic.edit.UpdateView):
    model = Shop
    fields = "__all__"


class DeleteView(generic.edit.DeleteView):
    model = Shop
    success_url = reverse_lazy("main:index")
