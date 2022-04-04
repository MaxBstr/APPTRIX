from django.core import mail
from django.conf import settings

from math import sin, cos, radians, acos, trunc


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


def get_great_circle_distance(la_1, lo_1, la_2, lo_2):
    """
        :param la_1: first_client_latitude in degrees
        :param lo_1: first_client_longitude in degrees
        :param la_2: second_client_latitude in degrees
        :param lo_2: second_client_longitude in degrees
        :return: distance
    """

    earth_radius = 6_400_000  # in metres

    la_1, lo_1 = map(radians, (float(la_1), float(lo_1)))
    la_2, lo_2 = map(radians, (la_2, lo_2))
    coefficient = acos(
        cos(la_1) * cos(la_2) * cos(lo_1 - lo_2) +
        sin(la_1) * sin(la_2)
    )
    distance = earth_radius * coefficient

    return abs(trunc(distance))
