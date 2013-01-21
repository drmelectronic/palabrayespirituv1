# -*- coding: utf-8 -*-
import os, sys
os.environ['DJANGO_SETTINGS_MODULE']='servidor.settings'
sys.path+=[os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]]
from kids.models import *
from django.contrib.auth.models import User
import datetime

daniel = User.objects.get(id=1)
daniel.username = "daniel"
daniel.first_name = "Daniel"
daniel.last_name = "Robles Martínez"
daniel.save()
pamela = User(
    username="pamela",
    first_name="Pamela",
    last_name="Reyes Enciso",
    email='pameladrm@gmail.com')
try:
    pamela.save()
except:
    pamela = User.objects.get(username='pamela')
guadalupe = User(
    username="guadalupe",
    first_name="Guadalupe",
    last_name="Enciso Calvo",
    email='@gmail.com')
try:
    guadalupe.save()
except:
    guadalupe = User.objects.get(username='guadalupe')
robert = User(
    username="robert",
    first_name="Robert",
    last_name="Robles Martínez",
    email='rrobertdan@gmail.com')
try:
    robert.save()
except:
    robert = User.objects.get(username='robert')
tim = User(
    username="tim",
    first_name="Tim",
    last_name="Robles Martínez",
    email='robles_tim@gmail.com')
try:
    tim.save()
except:
    tim = User.objects.get(username='tim')
ronald = User(
    username="ronald",
    first_name="Ronald",
    last_name="Robles Martínez",
    email='brain248@hotmail.com')
try:
    ronald.save()
except:
    ronald = User.objects.get(username='ronald')

daniel_profile = UserProfile(
    user=daniel,
    direccion="Jr. San Lucas 211 Urb. Palao - SMP",
    celular=969334754,
    nacimiento=datetime.date(1987, 5, 6))
daniel_profile.save()
pamela_profile = UserProfile(
    user=pamela,
    direccion="Jr. San Lucas 211 Urb. Palao - SMP",
    celular=969334753,
    nacimiento=datetime.date(1987, 12, 28))
pamela_profile.save()
guadalupe_profile = UserProfile(
    user=guadalupe,
    direccion="Jr. San Lucas 211 Urb. Palao - SMP",
    celular=987653242,
    nacimiento=datetime.date(1987, 5, 6))
guadalupe_profile.save()
robert_profile = UserProfile(
    user=robert,
    direccion="Jr.Algarrobos 211 Urb. Los Jardines - SMP",
    celular=969334755,
    nacimiento=datetime.date(1981, 5, 25))
robert_profile.save()
tim_profile = UserProfile(
    user=tim,
    direccion="Jr.Algarrobos 211 Urb. Los Jardines - SMP",
    celular=962387271,
    nacimiento=datetime.date(1993, 4, 6))
tim_profile.save()
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
    nombre=Hoja,
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

francesca = User(
    username="francesca",
    first_name="Francesca",
    last_name="Reyes Remigio",
    email='chocotita40@hotmail.com')
francesca.save()
francesca_profile = UserProfile(
    user=francesca,
    direccion="Jr.Algarrobos 211 Urb. Los Jardines - SMP",
    celular=969334754,
    nacimiento=datetime.date(2000, 10, 6))
francesca_profile.save()