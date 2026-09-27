from django.views.generic import TemplateView

from config import CLIENTKEY as PATH


from django.contrib import admin
from django.urls import path, include
from . import views
app_name = "Client"
urlpatterns = [
    path("", views.HomepageView.as_view(), name="homepage"),
    path("consultation/", views.ConsultationView.as_view(), name="consultation"),
    path("login/", views.LoginView.as_view(), name="login"),
    # path("property/", views.PropertyView.as_view(), name="property"),
    path("order/<int:order_id>/", views.OrderView.as_view(), name="order"),
    # path("update_order_status/<int:order_id>/", views.update_order_status, name="update_order_status"),

    path("booking/", views.BookingView.as_view(), name="booking"),
    path("orders/", views.OrdersView.as_view(), name="orders"),
    # path("booking/<str:key>/<str:type>/",views.BookingView.as_view(),name="booking_with_data",),
]
