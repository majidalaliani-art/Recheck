from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
from Admin.mixins import AdminRequiredMixin


class AdminDashboardView(AdminRequiredMixin, TemplateView):
    template_name = 'Admin/dashboard.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
