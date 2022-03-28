from django.core import mail
from django.conf import settings


def send_mail(sender, recipient):
    """
        Send mail to client when double match
    """

    mail_subject = f'Hello, {sender.first_name}!'
    mail_message = f'You got match with user: {recipient.first_name}!\n' \
                   f'Yours partner email: {recipient.email}'

    mail.send_mail(
        mail_subject,
        mail_message,
        settings.EMAIL_HOST_USER,
        [sender.email],
        fail_silently=False,
    )
