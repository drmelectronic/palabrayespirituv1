from django.conf.urls import patterns, include, url
from django.views.generic import ListView, DetailView, UpdateView
from kids.views import *
from kids.models import *
from django.contrib import admin

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('kids.views',
    url(r'^$', 'salones'),
    url(r'^asistencia', 'asistencia'),
    url(r'^alumnos$', ListView.as_view(
        model=Alumno,
        context_object_name="alumnos")),
    url(r'^alumnos/(?P<pk>\d+)$', DetailView.as_view(
        model=Alumno,
        context_object_name="alumno")),
    url(r'^alumnos/editar/(?P<pk>\d+)$', UpdateView.as_view(
        model=Alumno,
        context_object_name="alumno",
        success_url='/kids/alumnos')),
    url(r'^alumnos/crear$', AlumnoCreateView.as_view()),
    url(r'^userprofile/(?P<pk>\d+)$', UpdateView.as_view(
        model=UserProfile,
        context_object_name="alumno",
        success_url='/kids/alumnos/',
        template_name='kids/userprofile_form.html')),
    url(r'^salon/(?P<pk>\d+)$', SalonAlumnosListView.as_view()),
    url(r'^punto$', 'punto'),
    url(r'^admin/', include(admin.site.urls)),
)
