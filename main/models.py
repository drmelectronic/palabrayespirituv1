# -*- encoding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    """Datos adicionales del Usuario"""
    user = models.OneToOneField(User)
    direccion = models.CharField(max_length=128, null=True, default=None)
    celular = models.CharField(max_length=10, null=True, default=None)
    nacimiento = models.DateField(null=True, default=None)

    def __unicode__(self):
        return self.user.first_name
