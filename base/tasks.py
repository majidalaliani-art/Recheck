from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
@shared_task
def send_password_reset_email_task(subject, body, from_email, to_email, html_email=None):
    recipient_list = [to_email] if isinstance(to_email, str) else to_email
    from_email = from_email or settings.DEFAULT_FROM_EMAIL
    email = EmailMultiAlternatives(subject=subject,body=body,from_email=from_email,to=recipient_list)
    if html_email:
        email.attach_alternative(html_email, "text/html")
    email.send(fail_silently=True)
    
