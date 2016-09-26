from django.contrib import admin
from .models import PerfilUsuario

# Register your models here.


class PerfilUsuarioAdmin(admin.ModelAdmin):
    fields = ['username', 'first_name', 'last_name', 'password', 'groups', 'tipo_id', 'identificacion',
              'fecha_nacimiento', 'genero', 'email', 'foto']
    empty_value_display = '-empty-'
    date_hierarchy = 'last_login'

admin.site.register(PerfilUsuario, PerfilUsuarioAdmin)
