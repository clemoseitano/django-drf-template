import json
import logging
import os
import time

from django.template.loader import render_to_string
from django_celery_beat.models import PeriodicTask

from celery import shared_task

logger = logging.getLogger()


@shared_task(
    email="", subject="", template_name="", template_fields_json_str="{}", message_id=""
)
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

    logger.debug(f"Sending emails to {email}.")
    try:
        from_email = f"{os.environ.get('EMAIL_HOST_USER')}"
        message = render_to_string(template_name, json.loads(template_fields_json_str))
        is_sent = send_mail(
            subject,
            message,
            from_email,
            email.split(";"),
            fail_silently=False,
            html_message=message,
        )
        logger.debug(f"Email sent {is_sent}")
        # Remove task for sent email
        from django_celery_beat.models import PeriodicTask

        task = PeriodicTask.objects.filter(name=message_id).first()
        if is_sent != 0:
            task.enabled = False
        else:
            total = task.total_run_count + 1
            task.total_run_count = total
            if total >= 3:
                task.enabled = False
        task.save()
    except Exception as e:
        logger.debug(e)
