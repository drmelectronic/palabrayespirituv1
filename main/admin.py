# -*- encoding: utf-8 *-*

from django.contrib import admin
from kids.models import *


class AlumnoAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': [
            'user',
            'apoderado',
            'relacion',
            'telefono',
            'foto']
            }
        )
    ]
    list_display = ('user', 'telefono',)


class SalonAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': [
            'desde',
            'hasta']
            }
        )
    ]
    list_display = ('desde', 'hasta')


class UserProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': [
            'user',
            'direccion',
            'celular',
            'nacimiento']
            }
        )
    ]
    list_display = ('user', 'direccion')


admin.site.register(Alumno, AlumnoAdmin)
admin.site.register(Salon, SalonAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
