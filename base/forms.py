from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string  # <-- استدعاء مباشر
from .tasks import send_password_reset_email_task
from django.contrib.auth import get_user_model
from django.urls import reverse
User = get_user_model()

class AsyncPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def send_mail(self, subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name=None):
        if self.request:
            protocol = 'https' if self.request.is_secure() else 'http'
            domain = self.request.get_host()
        else:
            protocol = context.get('protocol', 'http')
            domain = context.get('domain')

        uid = context.get('uid')
        token = context.get('token')
        path = reverse('Base:password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
        context['reset_url'] = f"{protocol}://{domain}{path}"

        subject = render_to_string(subject_template_name, context).strip()
        body = render_to_string(email_template_name, context)

        html_email = None
        if html_email_template_name:
            html_email = render_to_string(html_email_template_name, context)
        send_password_reset_email_task.delay(subject=subject,body=body,from_email=from_email,to_email=to_email,html_email=html_email,)
