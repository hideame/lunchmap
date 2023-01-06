from django.urls import reverse_lazy
from django.views import generic

from .models import Category, Shop


class IndexView(generic.ListView):
    model = Shop
