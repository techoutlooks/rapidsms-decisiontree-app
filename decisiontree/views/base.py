"""Common logic for CRUD views used in rapidsms-decisiontree."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.generic import DeleteView, DetailView, ListView, UpdateView
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import ModelFormMixin, ProcessFormView


def cbv_decorator(function_decorator):
    """Allows a function-based decorator to be used on a class-based View."""

    def class_decorator(View):
        View.dispatch = method_decorator(function_decorator)(View.dispatch)
        return View
    return class_decorator


class SuccessMessageMixin(object):
    """Add a user message when an action is successfully completed."""
    success_message = None
    success_message_level = messages.INFO

    def get_success_message(self):
        if self.success_message:
            return self.success_message.format(obj=self.object)
        return None

    def get_success_url(self):
        message = self.get_success_message()
        if message:
            messages.add_message(self.request, self.success_message_level, message)
        return super(SuccessMessageMixin, self).get_success_url()


@cbv_decorator(login_required)
class TreeListView(ListView):
    limit = None
    order_by = None
    select_related = None

    def get_queryset(self):
        qs = super(TreeListView, self).get_queryset()
        if self.select_related is not None:
            qs = qs.select_related(*self.select_related)
        if self.order_by is not None:
            qs = qs.order_by(*self.order_by)
        if self.limit is not None:
            qs = qs[:self.limit]
        return qs


@cbv_decorator(login_required)
class TreeDetailView(DetailView):
    pass


@cbv_decorator(login_required)
@cbv_decorator(transaction.atomic)
class TreeUpdateView(SuccessMessageMixin, UpdateView):
    pass


@cbv_decorator(login_required)
@cbv_decorator(transaction.atomic)
class TreeCreateUpdateView(SuccessMessageMixin, SingleObjectTemplateResponseMixin,
                           ModelFormMixin, ProcessFormView):
    """Combines logic for UpdateView and CreateView."""
    create_success_message = None
    edit_success_message = None
    template_suffix_name = "_form"

    def get(self, request, *args, **kwargs):
        self.set_object(request, *args, **kwargs)
        return super(TreeCreateUpdateView, self).get(request, *args, **kwargs)

    def get_success_message(self):
        if self.mode == "edit" and self.edit_success_message:
            return self.edit_success_message.format(obj=self.object)
        elif self.mode == "create" and self.create_success_message:
            return self.create_success_message.format(obj=self.object)
        return None

    def post(self, request, *args, **kwargs):
        self.set_object(request, *args, **kwargs)
        return super(TreeCreateUpdateView, self).post(request, *args, **kwargs)

    def set_object(self, request, *args, **kwargs):
        if kwargs.get(self.pk_url_kwarg) or kwargs.get(self.slug_url_kwarg):
            self.mode = "edit"
            self.object = self.get_object()
        else:
            self.mode = "create"
            self.object = None


@cbv_decorator(login_required)
@cbv_decorator(transaction.atomic)
class TreeDeleteView(SuccessMessageMixin, DeleteView):
    http_method_names = ['post', 'delete']
