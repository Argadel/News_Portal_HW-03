from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import PostCategory
from .tasks import send_email


@receiver(m2m_changed, sender=PostCategory)
def notification(sender, instance, **kwargs):
    if kwargs["action"] == 'post_add':
        categories = instance.category.all()
        subscribers = []
        for category in categories:
            subscribers += category.subscribers.all()

        subscribers = [s.email for s in subscribers]

        send_email.delay(instance.preview(), instance.pk, instance.title, subscribers)




