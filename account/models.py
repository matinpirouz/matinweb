from django.db import models

class BaleAccount(models.Model):
    user_id = models.CharField(max_length=255, unique=True)
    bale_id = models.CharField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"BaleAccount(user_id={self.user_id}, bale_id={self.bale_id}, phone_number={self.phone_number})"
    
from django.utils import timezone
from datetime import timedelta

def default_expiration():
    return timezone.now() + timedelta(minutes=10)

class BaleToken(models.Model):
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    bale_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    token = models.CharField(max_length=512, blank=True)
    received_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField(default=default_expiration)
    device_identifier = models.CharField(max_length=255, null=True, blank=True)




