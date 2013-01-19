from django.conf.urls import patterns, include, url
from django.views.generic import ListView


urlpatterns = patterns('main.views',
    url(r'^$', 'index'),
    url(r'^ingresar$', 'ingresar'),
)
