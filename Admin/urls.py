from django.urls import path
from . import views

app_name = "Admin"

urlpatterns = [
    path('dashboard/', views.AdminDashboardView.as_view(), name='dashboard'),
]
