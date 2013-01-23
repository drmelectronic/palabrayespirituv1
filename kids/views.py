# -*- encoding: utf-8 -*-
from kids.models import *
from kids.forms import *
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, FormView
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
import datetime


def salones(request):
    salones = Salon.objects.all()
    return render_to_response('kids/salones.html',
        {'salones': salones}, RequestContext(request))


@login_required
def asistencia(request):
    try:
        alumno_id = request.GET['alumno']
    except:
        return HttpResponseRedirect(reverse('kids.views.salones', args=()))
    else:
        diahora = datetime.datetime.now()
        dia = diahora.date()
        hora = diahora.time()
        if hora > datetime.time(12, 0, 0):
            parque = False
        else:
            parque = True
        w = dia.isoweekday()
        user = request.user
        profile = user.get_profile()
        alumno = get_object_or_404(Alumno, pk=int(alumno_id))
        asistencia = Asistencia.objects.filter(
            alumno=alumno_id,
            dia=dia,
            parque=parque
        )
        salones = alumno.salon_set.all()
        for s in salones:
            if parque == s.parque:
                salon = s
        if len(asistencia) == 0 and w == 7:
            asistencia = Asistencia(
                alumno=alumno,
                profesor=profile,
                parque=parque)
            asistencia.save()
        return HttpResponseRedirect('/kids/salon/' + str(salon.id))


class SalonAlumnosListView(ListView):
    context_object_name = "alumnos"
    template_name = "kids/alumnos_salon.html"

    def get_queryset(self):
        salon = get_object_or_404(Salon, id=self.kwargs['pk'])
        alumnos = salon.alumnos
        return alumnos

    def get_context_data(self, **kwargs):
        context = super(SalonAlumnosListView, self).get_context_data(**kwargs)
        dia = datetime.date.today()
        w = dia.isoweekday()
        if w != 7:
            dia -= datetime.timedelta(w)
        context['dia'] = dia
        return context

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
        self.success_url = '/kids/salon/' + str(alumno.salon.id)
        return super(AlumnoCreateView, self).form_valid(form)
