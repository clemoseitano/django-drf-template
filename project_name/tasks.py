import json
import time

from django.template.loader import render_to_string

from celery import shared_task


@shared_task(email="", subject="", template_name="", template_fields_json_str="{}", message_id="")
def send_mails(email, subject, template_name, template_fields_json_str, message_id):
    """
    Send mails to users
    @param email: A semicolon separated list of recipients
    @param subject: The subject of the email
    @param template_name: The name of the template to use
    @param template_fields_json_str: The fields and values of the template to use as a
    JSON parseable string
    @param message_id: An identifier for the task

    """
    from django.core.mail import send_mail
    from django.conf import settings

    message = render_to_string(template_name, json.loads(template_fields_json_str))

    is_sent = send_mail(
        subject=subject,
        message=message,
        recipient_list=email.split(";"), fail_silently=False, from_email=None)
    print(f"Email sent {is_sent}")

    # Remove task for sent email
    if is_sent:
        from django_celery_beat.models import PeriodicTask
        task = PeriodicTask.objects.filter(name=message_id)
        task.delete()
