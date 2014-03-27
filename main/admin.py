# -*- encoding: utf-8 *-*

from django.contrib import admin
from kids.models import *


class AlumnoAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': [
            'profile',
            'apoderado',
            'relacion',
            'telefono',
            'foto']
            }
        )
    ]
    list_display = ('profile', 'telefono',)


class SalonAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': [
            'desde',
            'hasta']
            }
        )
    ]
    list_display = ('desde', 'hasta')


class ClaseAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': [
            'orden',
            'nombre',
            'versiculo',
            'bosquejo',
            'temas',
            'memorizar',
            'ejercicios',
            'imagen',
            'preguntas',
            'historia',
            'verdad',
            ]
            }
        )
    ]
    list_display = ('orden', 'nombre', 'versiculo')


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
admin.site.register(Clase, ClaseAdmin)
admin.site.register(Salon, SalonAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
