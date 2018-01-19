from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from jsonfield import JSONField
from rest_framework.authtoken.models import Token


class Event(models.Model):
    event_type = models.CharField(max_length=255)
    data = JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, default='submitted',
                              choices=(('submitted', 'submitted'),
                                       ('processed', 'processed'),
                                       ('ignored', 'ignored')))

    class Meta:
        ordering = ['-timestamp']


# Create API tokens for new users
# via http://www.django-rest-framework.org/api-guide/authentication/#by-using-signals
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(
            user=instance,
            key=get_random_string(4),
        )