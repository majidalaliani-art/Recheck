from django.contrib import admin
from django.urls import path, include,reverse_lazy
from . import views
from Client import ajax as client_ajax
from django.views.generic import TemplateView

from django.contrib.auth import views as auth_views
from .constants import PATH
from .forms import AsyncPasswordResetForm

app_name = "Base"
urlpatterns = [
    path("upload_single_file/", views.upload_single_file, name="upload_single_file"),
   # path("create_card/", views.create_card, name="create_card"),
    path("visit_price/", client_ajax.visit_price, name="visit_price"),
    path("consultation_day/", client_ajax.consultation_day, name="consultation_day"),
    path("terms/", TemplateView.as_view(template_name=PATH["TERMS"]), name="terms"),
    path("privacy/", TemplateView.as_view(template_name=PATH["PRIVACY"]), name="privacy"),
    path("cancelation/", TemplateView.as_view(template_name=PATH["CANCELATION"]), name="cancelation"),
    path("inspector/",TemplateView.as_view(template_name=PATH["INSPECTOR"]), name="inspector"),
    path("logout/", views.logout_view, name="logout"),



    path('staff/login/', views.MyLoginView.as_view(), name='login'),


path(
    'password-reset/',
    auth_views.PasswordResetView.as_view(
        form_class=AsyncPasswordResetForm,
        template_name=PATH['PASSWORD_RESET'],
        email_template_name=PATH['PASSWORD_RESET_EMAIL'],
        subject_template_name=PATH['PASSWORD_RESET_SUBJECT'],
        success_url=reverse_lazy('Base:password_reset_done')
    ),
    name='password_reset'
),






path(
    'password-reset/done/',
    auth_views.PasswordResetDoneView.as_view(
        template_name=PATH['PASSWORD_RESET_DONE']
    ),
    name='password_reset_done'
),


path(
    'password-reset-confirm/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(
        template_name=PATH['PASSWORD_RESET_CONFIRM'],
        success_url=reverse_lazy('Base:password_reset_complete')
    ),
    name='password_reset_confirm'
),


path(
    'password-reset-complete/',
    auth_views.PasswordResetCompleteView.as_view(
        template_name=PATH['PASSWORD_RESET_COMPLETE']
    ),
    name='password_reset_complete'
),

]
