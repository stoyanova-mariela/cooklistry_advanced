from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_welcome_email(email, username):
    return send_mail(
        subject='Welcome to Cooklistry!',
        message=(
            f'Hello, {username}!\n\n'
            'Welcome to Cooklistry!\n'
            'Discover delicious recipes, create meal plans '
            'and share your culinary experiences.\n\n'
            'Happy cooking!\n'
            'The Cooklistry Team'
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
