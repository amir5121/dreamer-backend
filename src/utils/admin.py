from django.contrib import admin
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin


class DreamerAdmin(admin.ModelAdmin, DynamicArrayMixin):
    def get_queryset(self, request):
        if hasattr(self.model, "all_objects"):
            qs = self.model.all_objects.get_queryset()
        else:
            qs = self.model.objects.get_queryset()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs
