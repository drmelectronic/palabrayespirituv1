# -*- encoding: utf-8 -*-
from kids.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render_to_response, get_object_or_404, redirect

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout


def index(request):
    """Muestra una lista de Clientes"""
    return HttpResponse('Hola inicio'
    )


def ingresar(request):
    """Login"""
    if request.method == 'POST':
        formulario = AuthenticationForm(request.POST)
        if formulario.is_valid:
            usuario = request.POST['username']
            clave = request.POST['password']
            acceso = authenticate(username=usuario, password=clave)
            if acceso is not None:
                if acceso.is_active:
                    login(request, acceso)
                    return HttpResponseRedirect('/kids/')
                else:
                    return render_to_response(
                        'main/noactivo.html',
                        context_instance=RequestContext(request)
                    )
            else:
                return render_to_response(
                    'main/nousuario.html',
                    context_instance=RequestContext(request)
                )
    else:
        formulario = AuthenticationForm()
    return render_to_response(
        'main/ingresar.html',
        {'formulario': formulario},
        context_instance=RequestContext(request)
    )
