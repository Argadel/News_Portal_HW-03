from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from .models import Post


@shared_task
def send_email(preview, pk, title, subscribers):
    html_content = render_to_string(
        'post_created_emails.html',
        {'text': preview,
        'link': f'{settings.SITE_URL}/news/{pk}'
         })

    message = EmailMultiAlternatives(subject=title, body='', from_email=settings.DEFAULT_FROM_EMAIL, to=subscribers)

    message.attach_alternative(html_content, 'text/html')
    message.send()


@shared_task
def send_emails_to_users():
    users = User.objects.all()
    users_emails = []
    for user in users:
        users_emails.append(user.email)

    last_post = Post.objects.last()

    html_content = render_to_string(
        'weekly_emails.html',
        {'text': last_post.preview,
         'link': f'{settings.SITE_URL}/news/{last_post.pk}'
         })

    message = EmailMultiAlternatives(subject='Weekly news!', body='', from_email=settings.DEFAULT_FROM_EMAIL, to=users_emails)

    message.attach_alternative(html_content, 'text/html')
    message.send()

send_emails_to_users.delay()
