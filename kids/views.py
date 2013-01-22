# -*- encoding: utf-8 -*-
from kids.models import *
from kids.forms import *
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, FormView
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
import datetime


def salones(request):
    salones = Salon.objects.all()
    return render_to_response('kids/salones.html',
        {'salones': salones})


@login_required
def asistencia(request):
    try:
        alumno_id = request.GET['alumno']
    except:
        return HttpResponseRedirect(reverse('kids.views.salones', args=()))
    else:
        user = request.user
        profile = user.get_profile()
        alumno = get_object_or_404(Alumno, pk=int(alumno_id))
        asistencia = Asistencia.objects.filter(
            alumno=alumno_id,
            dia=datetime.date.today(),
        )
        if len(asistencia) == 0:
            template_name = 'kids/asistencia.html'
            asistencia = Asistencia(alumno=alumno,
                profesor=profile)
            asistencia.save()
        else:
            template_name = 'kids/ya-registrado.html'
        return render_to_response(
            template_name,
            {'alumno': alumno}
            )


class SalonAlumnosListView(ListView):
    context_object_name = "alumnos"
    template_name = "kids/alumnos_salon.html"

    def get_queryset(self):
        salon = get_object_or_404(Salon, id=self.kwargs['pk'])
        alumnos = Alumno.objects.filter(salon=salon)
        return alumnos


class AlumnoCreateView(FormView):
    form_class = AlumnoProfileForm
    template_name = 'kids/alumno_new.html'
    success_url = '/kids/alumnos'

    def form_valid(self, form):
        usuario = User(
            username=form.cleaned_data['usuario'],
            first_name=form.cleaned_data['nombres'],
            last_name=form.cleaned_data['apellidos'],
            email=form.cleaned_data['email'])
        usuario.save()
        profile = UserProfile(
            user=usuario,
            direccion=form.cleaned_data['direccion'],
            celular=form.cleaned_data['celular'],
            nacimiento=form.cleaned_data['nacimiento'])
        profile.save()
        alumno = Alumno(
            user=profile,
            apoderado=form.cleaned_data['apoderado'],
            relacion=form.cleaned_data['relacion'],
            telefono=form.cleaned_data['telefono'],
            foto=form.cleaned_data['foto'],
            salon=form.cleaned_data['salon'],
            observacion=form.cleaned_data['observacion'])
        alumno.save()
        return super(AlumnoCreateView, self).form_valid(form)
