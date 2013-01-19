from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('main.urls')),
    url(r'^kids/', include('kids.urls')),
    url(r'^comments/', include('django.contrib.comments.urls')),

    # Examples:
    # url(r'^$', 'servidor.views.home', name='home'),
    # url(r'^servidor/', include('servidor.foo.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
