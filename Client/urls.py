from django.urls import path
from . import views

app_name = "Client"

urlpatterns = [
    path("", views.HomepageView.as_view(), name="homepage"),
    path("consultation/", views.ConsultationView.as_view(), name="consultation"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("order/<str:order_id>/", views.OrderView.as_view(), name="order"),
    path("booking/", views.BookingView.as_view(), name="booking"),
    path("orders/", views.OrdersView.as_view(), name="orders"),
]
