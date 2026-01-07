from django.db import models
from django.utils import timezone
from datetime import timedelta


class BaleAccount(models.Model):
    user_id = models.CharField(max_length=255, unique=True)
    bale_id = models.CharField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.phone_number


def default_expiration():
    return timezone.now() + timedelta(minutes=10)


class BaleToken(models.Model):
    token = models.CharField(max_length=512, unique=True)
    device_identifier = models.CharField(max_length=255)

    phone_number = models.CharField(max_length=20, null=True, blank=True)
    bale_id = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField(default=default_expiration)

    def is_expired(self):
        return self.expiration_date < timezone.now()

    def __str__(self):
        return self.token
