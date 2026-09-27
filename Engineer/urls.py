from django.contrib import admin
from django.urls import path, include
from . import views
from django.urls import path


app_name = "Staff"




urlpatterns = [
    path("careers/", views.ApplyView.as_view(), name="apply"),
    path("join/", views.SignUpView.as_view(), name="register"),
    path("staff/settings/", views.SettingsView.as_view(), name="settings"),




    path('staff/order/<str:type>/<int:pk>/', views.OrderDetailView.as_view(), name='order_progress'),


    path("staff/orders/available/", views.OrdersOverviewView.as_view(), name="available_orders"),


    path("staff/orders/inprogress/", views.OrdersOverviewView.as_view(), name="in_progress_orders"),
    path("staff/orders/review/", views.OrdersOverviewView.as_view(), name="under_review_orders"),


    path("staff/orders/completed", views.OrdersOverviewView.as_view(), name="completed_orders"),

    path("staff/data/", views.staffDataView.as_view(), name="staff_data"),

    path("staff/wallet/", views.WalletView.as_view(), name="wallet"),



]
