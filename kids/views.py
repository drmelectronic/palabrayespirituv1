# -*- encoding: utf-8 -*-
from kids.models import *
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render_to_response, get_object_or_404, redirect
import datetime


def salones(request):
    salones = Salon.objects.all()
    return render_to_response('kids/salones.html',
        {'salones': salones})


def asistencia(request):
    try:
        alumno_id = request.GET['alumno']
    except:
        return HttpResponseRedirect(reverse('kids.views.salones', args=()))
    else:
        alumno = get_object_or_404(Alumno, pk=int(alumno_id))
        asistencia = Asistencia.objects.filter(
            alumno=alumno_id,
            dia=datetime.date.today()
        )
        if len(asistencia) == 0:
            template_name = 'kids/asistencia.html'
            asistencia = Asistencia(alumno=alumno)
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
        salon = get_object_or_404(Salon, id=self.args[0])
        alumnos = Alumno.objects.filter(
            nacimiento__lte=datetime.date.today() - salon.hasta,
            nacimiento__gte=datetime.date.today() - salon.desde)
        return alumnos
