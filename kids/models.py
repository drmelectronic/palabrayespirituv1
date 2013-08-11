# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from main.models import *
import datetime
from PIL import Image
import os

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
    orden = models.PositiveSmallIntegerField()
    nombre = models.CharField(max_length=32)
    versiculo = models.CharField(max_length=256)
    bosquejo = models.CharField(max_length=1024 * 8)
    temas = models.CharField(max_length=1024)
    memorizar = models.CharField(max_length=256)
    ejercicios = models.CharField(max_length=1024)
    imagen = models.ImageField(upload_to='kids/colorear/')
    preguntas = models.CharField(max_length=1024)
    historia = models.CharField(max_length=2048, blank=True, null=True)
    verdad = models.CharField(max_length=256)

    def __unicode__(self):
        return self.nombre


class Profesor(models.Model):
    profile = models.OneToOneField(UserProfile)


class ApoderadoTipo(models.Model):
    nombre = models.CharField(max_length=16, unique=True)

    def __unicode__(self):
        return self.nombre


class Alumno(models.Model):
    profile = models.OneToOneField(UserProfile)
    apoderado = models.CharField(max_length=64, null=True, default=None)
    relacion = models.ForeignKey(ApoderadoTipo)
    telefono = models.CharField(max_length=10, null=True, default=None)
    foto = models.ImageField(upload_to='alumnos')
    parque = models.BooleanField()
    ed = models.BooleanField()
    ingreso = models.DateField(auto_now=True)
    observacion = models.CharField(max_length=256, null=True, blank=True)

    def __unicode__(self):
        return self.profile.nombre()

    def asistio(self):
        dia = datetime.date.today()
        w = dia.isoweekday()
        if w != 7:
            dia -= datetime.timedelta(w)
        return bool(self.asistencia_set.filter(dia=dia))

    def asistencia(self):
        dia = datetime.date.today()
        w = dia.isoweekday()
        if w != 7:
            dia -= datetime.timedelta(w)
        return self.asistencia_set.get(dia=dia)

    def puntos(self):
        asistencia = self.asistencia()
        return asistencia.puntos()

    def thumb(self):
        p = self.foto.url
        raiz = p[:-4]
        return raiz + '-thumb.' + p[-3:]

    def edad(self):
        h = datetime.date.today()
        n = self.profile.nacimiento
        i = -1
        while n < h:
            n = datetime.date(n.year + 1, n.month, n.day)
            i += 1
        return i

    def save(self):
        super(Alumno, self).save()
        image = Image.open(self.foto)
        p = self.foto.path
        p_ant = p
        e = os.path.splitext(p)[1]
        if 'j' in e or 'J' in e:
            e = '.jpg'
        elif 'n' in e or 'N' in e:
            e = '.png'
        elif 'i' in e or 'I' in e:
            e = '.gif'
        nombre = str(self.id)
        b = os.path.split(p)[0]
        p = '%s/%s%s' % (b, nombre, e)
        url = str(self.foto)
        url = os.path.split(url)[0] + '/' + nombre + e
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
        thumbnail.save(b + '/' + nombre + '-thumb' + e)
        salones = Salon.objects.all()
        edad = self.edad()
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
        self.foto = url
        os.remove(p_ant)
        super(Alumno, self).save()


class Nomina(models.Model):
    alumno = models.ForeignKey(Alumno)
    salon = models.ForeignKey(Salon)

    class Meta:
        unique_together = (('alumno', 'salon'),)


class Asistencia(models.Model):
    alumno = models.ForeignKey(Alumno)
    dia = models.DateField(auto_now=True)
    profesor = models.ForeignKey(UserProfile)
    parque = models.BooleanField()

    def __unicode__(self):
        return str(self.alumno) + ': ' + str(self.dia)

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

    def __unicode__(self):
        return self.nombre


class Punto(models.Model):
    asistencia = models.ForeignKey(Asistencia)
    motivo = models.ForeignKey(PuntoMotivo)
    profesor = models.ForeignKey(UserProfile)
