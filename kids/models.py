# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from main.models import *
import datetime
from PIL import Image

# Create your models here.


class Salon(models.Model):
    desde = models.PositiveSmallIntegerField()
    hasta = models.PositiveSmallIntegerField()
    parque = models.BooleanField()

    def __unicode__(self):
        return str(self.desde) + ' - ' + str(self.hasta)

    def alumnos(self):
        nominas = self.nomina_set.all()
        alumnos = []
        for n in nominas:
            alumnos.append(n.alumno)
        return alumnos


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
    parque = models.BooleanField()
    ed = models.BooleanField()
    ingreso = models.DateField()
    observacion = models.CharField(max_length=256, null=True, blank=True)

    def __unicode__(self):
        return self.user

    def asistio(self):
        dia = datetime.date.today()
        w = dia.isoweekday()
        if w != 7:
            dia -= datetime.timedelta(w)
        return bool(self.asistencia_set.filter(dia=dia))

    def thumb(self):
        p = self.foto.url
        return p + '.thumb.' + p[-3:]

    def save(self):
        edad = self.edad
        if edad > 12:
            return False
        super(Alumno, self).save()
        p = self.foto.path
        image = Image.open(self.foto)
        (width, height) = image.size
        "Max width and height 800"
        fx = 800. / width
        fy = 800. / height
        factor = min(fx, fy)
        size = (int(width * factor), int(height * factor))
        thumb_size = (int(width * factor / 16), int(height * factor / 16))
        thumbnail = image.resize(thumb_size, Image.ANTIALIAS)
        image = image.resize(size, Image.ANTIALIAS)
        image.save(p)
        thumbnail.save(p + '.thumb.' + p[-3:])
        salones = Salon.objects.all()
        if self.parque:
            for s in salones:
                if s.desde <= edad and edad <= s.hasta and s.parque:
                    salon = s
            nomina = Nomina(
                alumno=self,
                salon=salon)
            nomina.save()
        if self.ed:
            for s in salones:
                if s.desde <= edad and edad <= s.hasta and not s.parque:
                    salon = s
            nomina = Nomina(
                alumno=self,
                salon=salon)
            nomina.save()


class Nomina(models.Model):
    alumno = models.ForeignKey(Alumno)
    salon = models.ForeignKey(Salon)

    class Meta:
        unique_together = (('alumno', 'salon'),)


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
