from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views import generic

from .models import Shop


class IndexView(generic.ListView):
    model = Shop


class DetailView(generic.DetailView):
    model = Shop


class CreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Shop
    fields = ["name", "address", "category"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CreateView, self).form_valid(form)


class UpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Shop
    fields = ["name", "address", "category"]

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        print(obj.author)
        print(self.request.user)
        if obj.author != self.request.user:
            raise PermissionDenied("You do not have permission to edit.")
        return super(UpdateView, self).dispatch(request, *args, **kwargs)


class DeleteView(LoginRequiredMixin, generic.edit.DeleteView):
    model = Shop
    success_url = reverse_lazy("main:index")

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        print(obj.author)
        print(self.request.user)
        if obj.author != self.request.user:
            raise PermissionDenied("You do not have permission to delete.")
        return super(DeleteView, self).dispatch(request, *args, **kwargs)
