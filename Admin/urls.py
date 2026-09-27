from django.views.generic import TemplateView

from config import CLIENTKEY as PATH


from django.contrib import admin
from django.urls import path, include
from . import views
app_name = "Admin"
urlpatterns = [
    path('dashboard/', views.AdminDashboardView.as_view(), name='dashboard'),

]
