# -*- coding: utf-8 *-*
from django import forms
from kids.models import *


class AlumnoProfileForm(forms.Form):
    usuario = forms.CharField(max_length=16, required=True)
    nombres = forms.CharField(max_length=32, required=True)
    apellidos = forms.CharField(max_length=64, required=True)
    email = forms.EmailField(max_length=64, required=False)
    direccion = forms.CharField(max_length=128, required=False)
    celular = forms.CharField(max_length=10, required=False)
    nacimiento = forms.DateField(required=False)
    apoderado = forms.CharField(max_length=16, required=False)
    relacion = forms.ModelChoiceField(
        ApoderadoTipo.objects.all(),
        empty_label=None,
        required=False)
    telefono = forms.CharField(max_length=10, required=False)
    foto = forms.ImageField(required=False)
    salon = forms.ModelChoiceField(
        Salon.objects.all(),
        empty_label=None,
        required=True)
    observacion = forms.CharField(max_length=256, required=False,
        widget=forms.Textarea)
