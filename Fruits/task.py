from celery import shared_task

from Fruits.util import send_email


@shared_task
def send_activate_email_async(username, to_email):
    send_email(username, to_email)

