from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_email_task(subject: str, message: str, recipient_list: list, from_email='noreply@example.com'):
    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=False,
    )
