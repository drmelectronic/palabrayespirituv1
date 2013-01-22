# -*- coding: utf-8 -*-
import os
import sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'servidor.settings'
sys.path += [os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]]
from kids.models import *
from django.contrib.auth.models import User
import datetime

daniel = User.objects.get(id=1)
daniel.username = "daniel"
daniel.first_name = "Daniel"
daniel.last_name = "Robles Martínez"
daniel.save()
try:
    pamela = User.objects.get(username='pamela')
except:
    pamela = User(
    username="pamela",
    first_name="Pamela",
    last_name="Reyes Enciso",
    email='pameladrm@gmail.com')
    pamela.save()
try:
    guadalupe = User.objects.get(username='guadalupe')
except:
    guadalupe = User(
    username="guadalupe",
    first_name="Guadalupe",
    last_name="Enciso Calvo",
    email='@gmail.com')
    guadalupe.save()
try:
    robert = User.objects.get(username='robert')
except:
    robert = User(
    username="robert",
    first_name="Robert",
    last_name="Robles Martínez",
    email='rrobertdan@gmail.com')
    robert.save()
try:
    tim = User.objects.get(username='tim')
except:
    tim = User(
    username="tim",
    first_name="Tim",
    last_name="Robles Martínez",
    email='robles_tim@gmail.com')
    tim.save()
try:
    ronald = User.objects.get(username='ronald')
except:
    ronald = User(
    username="ronald",
    first_name="Ronald",
    last_name="Robles Martínez",
    email='brain248@hotmail.com')
    ronald.save()

try:
    daniel_profile = UserProfile.objects.get(user=daniel)
except:
    daniel_profile = UserProfile(
    user=daniel,
    direccion="Jr. San Lucas 211 Urb. Palao - SMP",
    celular=969334754,
    nacimiento=datetime.date(1987, 5, 6))
    daniel_profile.save()
try:
    pamela_profile = UserProfile.objects.get(user=pamela)
except:
    pamela_profile = UserProfile(
    user=pamela,
    direccion="Jr. San Lucas 211 Urb. Palao - SMP",
    celular=969334753,
    nacimiento=datetime.date(1987, 12, 28))
    pamela_profile.save()
try:
    guadalupe_profile = UserProfile.objects.get(user=guadalupe)
except:
    guadalupe_profile = UserProfile(
    user=guadalupe,
    direccion="Jr. San Lucas 211 Urb. Palao - SMP",
    celular=987653242,
    nacimiento=datetime.date(1987, 5, 6))
    guadalupe_profile.save()
try:
    robert_profile = UserProfile.objects.get(user=robert)
except:
    robert_profile = UserProfile(
    user=robert,
    direccion="Jr.Algarrobos 211 Urb. Los Jardines - SMP",
    celular=969334755,
    nacimiento=datetime.date(1981, 5, 25))
    robert_profile.save()
try:
    tim_profile = UserProfile.objects.get(user=tim)
except:
    tim_profile = UserProfile(
    user=tim,
    direccion="Jr.Algarrobos 211 Urb. Los Jardines - SMP",
    celular=962387271,
    nacimiento=datetime.date(1993, 4, 6))
    tim_profile.save()
try:
    ronald_profile = UserProfile.objects.get(user=ronald)
except:
    ronald_profile = UserProfile(
    user=ronald,
    direccion="Jr.Algarrobos 211 Urb. Los Jardines - SMP",
    celular=969334754,
    nacimiento=datetime.date(1983, 11, 15))
    ronald_profile.save()

salon1 = Salon(
    desde=0,
    hasta=2,
    parque=True)
salon1.save()
salon2 = Salon(
    desde=3,
    hasta=5,
    parque=True)
salon2.save()
salon3 = Salon(
    desde=6,
    hasta=7,
    parque=True)
salon3.save()
salon4 = Salon(
    desde=8,
    hasta=9,
    parque=True)
salon4.save()
salon5 = Salon(
    desde=10,
    hasta=12,
    parque=True)
salon5.save()
salon6 = Salon(
    desde=0,
    hasta=6,
    parque=False)
salon6.save()
salon7 = Salon(
    desde=7,
    hasta=12,
    parque=False)
salon7.save()

asistencia = PuntoMotivo(
    nombre="Asistencia",
    valor=1)
asistencia.save()
versiculo = PuntoMotivo(
    nombre="Versículo",
    valor=1)
versiculo.save()
hoja = PuntoMotivo(
    nombre="Hoja",
    valor=1)
hoja.save()
participa = PuntoMotivo(
    nombre="Participación",
    valor=1)
participa.save()
comporta = PuntoMotivo(
    nombre="Comportamiento",
    valor=1)
comporta.save()

apoderado = ApoderadoTipo(
    nombre="Mamá")
apoderado.save()
apoderado = ApoderadoTipo(
    nombre="Papá")
apoderado.save()
apoderado = ApoderadoTipo(
    nombre="Tío(a)")
apoderado.save()
apoderado = ApoderadoTipo(
    nombre="Abuelo(a)")
apoderado.save()
apoderado = ApoderadoTipo(
    nombre="Otro")
apoderado.save()

#try:
    #francesca = User.objects.get(username='francesca')
#except:
    #francesca = User(
        #username="francesca",
        #first_name="Francesca",
        #last_name="Reyes Remigio",
        #email='chocotita40@hotmail.com')
    #francesca.save()
#try:
    #francesca_profile = UserProfile.objects.get(user=francesca)
#except:
    #francesca_profile = UserProfile(
        #user=francesca,
        #direccion="Jr.Algarrobos 211 Urb. Los Jardines - SMP",
        #celular=969334754,
        #nacimiento=datetime.date(2000, 10, 6))
    #francesca_profile.save()
#
