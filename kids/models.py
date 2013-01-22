# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from main.models import *
import datetime

# Create your models here.


class Salon(models.Model):
    desde = models.PositiveSmallIntegerField()
    hasta = models.PositiveSmallIntegerField()
    parque = models.BooleanField()

    def __unicode__(self):
        return str(self.desde) + ' - ' + str(self.hasta)


class Clase(models.Model):
    nombre = models.CharField(max_length=32)
    versiculo = models.CharField(max_length=256)
    cita = models.CharField(max_length=32)
    ejercicios = models.CharField(max_length=1024)
    imagen = models.ImageField(upload_to='colorear')
    preguntas = models.CharField(max_length=1024)
    palabras = models.CharField(max_length=512)
    historia = models.CharField(max_length=2048)

    def __unicode__(self):
        return self.nombre


class ApoderadoTipo(models.Model):
    nombre = models.CharField(max_length=16, unique=True)

    def __unicode__(self):
        return self.nombre


class Alumno(models.Model):
    user = models.OneToOneField(UserProfile)
    apoderado = models.CharField(max_length=64, null=True, default=None)
    relacion = models.ForeignKey(ApoderadoTipo)
    telefono = models.CharField(max_length=10, null=True, default=None)
    foto = models.ImageField(upload_to='alumnos')
    salon = models.ForeignKey(Salon)
    observacion = models.CharField(max_length=256, null=True, blank=True)

    def __unicode__(self):
        return self.user

    def asistio(self):
        dia = datetime.date.today()
        return bool(self.asistencia_set.filter(dia=dia))


class Asistencia(models.Model):
    alumno = models.ForeignKey(Alumno)
    dia = models.DateField(auto_now=True)
    profesor = models.ForeignKey(UserProfile)

    def __unicode__(self):
        return self.alumno + ': ' + str(self.dia)

    def puntos(self):
        contador = 0
        puntos = self.punto_set.all()
        for p in puntos:
            contador += p.motivo.valor
        return contador

    class Meta:
        unique_together = (('alumno', 'dia'),)


class PuntoMotivo(models.Model):
    nombre = models.CharField(max_length=16, unique=True)
    valor = models.PositiveSmallIntegerField()


class Punto(models.Model):
    alumno = models.ForeignKey(Alumno)
    asistencia = models.ForeignKey(Asistencia)
    motivo = models.ForeignKey(PuntoMotivo)
    profesor = models.ForeignKey(UserProfile)
