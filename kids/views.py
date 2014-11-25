#! /usr/bin/python
# -*- encoding: utf-8 -*-

from kids.models import *
from kids.forms import *
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, FormView, UpdateView
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
import datetime
from kids.pdf import *
import servidor.claves
from django.conf import settings
import smtplib
import mimetypes
from email.message import Message
from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
        nomina = alumno.nomina_set.all()
        for n in nomina:
            if parque == n.salon.parque:
                salon = n.salon
        if len(asistencia) == 0 and w == 7:
            asistencia = Asistencia(
                alumno=alumno,
                profesor=profile,
                parque=parque)
            asistencia.save()
            motivo = PuntoMotivo.objects.get(id=1)
            punto = Punto(
                asistencia=asistencia,
                motivo=motivo,
                profesor=profile)
            punto.save()
        elif w != 7:
            return render_to_response('kids/error.html',
            {'error': 'No puede registrar asistencia si no es Domingo.'},
            RequestContext(request))
        return HttpResponseRedirect('/kids/salon/' + str(salon.id))


@login_required
def punto(request):
    try:
        asistencia_id = request.GET['asistencia']
        asistencia = get_object_or_404(Asistencia, id=asistencia_id)
        success = request.GET['next']
        motivo_id = request.POST['motivo']
        motivo = get_object_or_404(PuntoMotivo, id=motivo_id)
        profesor = request.user.get_profile()
    except:
        erorr = 3 + 'c'
        return HttpResponseRedirect(success)
    else:
        punto = Punto(
            asistencia=asistencia,
            motivo=motivo,
            profesor=profesor)
        punto.save()
        return HttpResponseRedirect(success)


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
        motivos = PuntoMotivo.objects.all()[1:]
        context['motivos'] = motivos
        context['salon'] = self.kwargs['pk']
        return context


class AlumnoCreateView(FormView):
    form_class = AlumnoProfileForm
    template_name = 'kids/view_new.html'
    success_url = '/kids/alumnos'

    def form_valid(self, form):
        diahora = datetime.datetime.now()
        hoy = diahora.date()
        limite = datetime.date(hoy.year - 12, hoy.month, hoy.day)
        if form.cleaned_data['nacimiento'] > limite:
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
                profile=profile,
                apoderado=form.cleaned_data['apoderado'],
                relacion=form.cleaned_data['relacion'],
                telefono=form.cleaned_data['telefono'],
                parque=form.cleaned_data['parque'],
                ed=form.cleaned_data['ed'],
                foto=form.cleaned_data['foto'],
                observacion=form.cleaned_data['observacion'])
            alumno.save()
            hora = diahora.time()
            if hora > datetime.time(12, 0, 0):
                parque = False
            else:
                parque = True
            nominas = alumno.nomina_set.all()
            salon_id = None
            for n in nominas:
                if parque == n.salon.parque:
                    salon_id = str(n.salon.id)
            if salon_id is None:
                self.success_url = '/'
            else:
                self.success_url = '/kids/salon/' + str(salon_id)
        return super(AlumnoCreateView, self).form_valid(form)



class ClaseCreateView(CreateView):
    form_class = ClaseForm
    template_name = 'kids/view_new.html'
    success_url = '/kids/clases'

    def form_valid(self, form):
        out = super(ClaseCreateView, self).form_valid(form)
        instance = form.instance        
        Guia(instance)
        return out

class ClaseUpdateView(UpdateView):    
    model = Clase
    form_class = ClaseForm
    context_object_name = "clase"
    success_url = '/kids/clases'

    def form_valid(self, form):
        out = super(ClaseUpdateView, self).form_valid(form)
        form.save()
        instance = form.instance
        t = instance.preguntas
        Guia(instance)
        return out

def compartir(request, pk):
    emails = ['drm.electronic@gmail.com', 'pameladrm@gmail.com',
    'robles.tim@gmail.com', 'brain248@hotmail.com', 'rrobles@econain.com',
    'rrobertdan@gmail.com']
    usuario = request.user.username.upper()
    clase = Clase.objects.get(id=pk)
    asunto = u'%s ha compartido la guía %s' % (usuario, clase.nombre)
    texto =  u'La guía %s ya está lista para que la estudies.' % clase.nombre
    archivos = (settings.MEDIA_ROOT + '/kids/guias/%d.pdf' % clase.id, )
    enviar_correo(emails, asunto, texto, archivos)
    return HttpResponseRedirect('/kids/clases')

def enviar_correo(emails, asunto, texto, archivos):
    msg = MIMEMultipart()
    msg['Subject'] = asunto
    msg['From'] = 'sistema@palabrayespiritu.org'
    msg['To'] = ', '.join(emails)
    msg.attach(MIMEText(texto, 'plain', 'UTF-8'))
    if not archivos is None:
        for archivo in archivos:
            ctype, encoding = mimetypes.guess_type(archivo)
            if ctype is None or encoding is not None:
                # No guess could be made, or the file is encoded (compressed), so
                # use a generic bag-of-bits type.
                ctype = 'application/octet-stream'
            maintype, subtype = ctype.split('/', 1)
            fp = open(archivo, 'rb')
            if maintype == 'text':
                # Note: we should handle calculating the charset
                adj = MIMEText(fp.read(), _subtype=subtype)
            elif maintype == 'image':
                adj = MIMEImage(fp.read(), _subtype=subtype)
            elif maintype == 'audio':
                adj = MIMEAudio(fp.read(), _subtype=subtype)
            else:
                adj = MIMEBase(maintype, subtype)
                adj.set_payload(fp.read())
                # Encode the payload using Base64
                encoders.encode_base64(adj)
            fp.close()
            # Set the filename parameter
            adj.add_header('Content-Disposition',
                    'attachment',
                    filename=os.path.basename(archivo))
            msg.attach(adj)
    # Autenticamos
    mailServer = smtplib.SMTP('smtp.gmail.com', 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.set_debuglevel(1)
    mailServer.login('sistema@palabrayespiritu.org', servidor.claves.mail)
    # Enviamos
    mailServer.sendmail('sistema@palabrayespiritu.org',
        emails,
        msg.as_string())
    # Cerramos conexion
    mailServer.close()
