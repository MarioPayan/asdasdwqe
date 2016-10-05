import operator

from django.views.generic import CreateView, UpdateView, DeleteView, View, DetailView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from utilities.datatables_tools.datatables_tools import DatatablesListView
from django.core.urlresolvers import reverse_lazy
from auditoria.loggers import (LoggerCreatedMixin, LoggerUpdatedMixin, LoggerGetMixin, LoggerViewMixin,
                               LoggerDeleteMixin)
from utilities.mixins import MessageMixin, GetToPostMixin
from django.contrib import messages

from .models import Persona
from .forms import PersonaForm


class PersonaCreateView(MessageMixin, PermissionRequiredMixin, LoggerCreatedMixin, CreateView):
    model = Persona
    form_class = PersonaForm
    permission_required = "personas.add_persona"
    raise_exception = True
    mensaje_log = "Creación de Persona"
    mensaje_exito = "Persona creado correctamente"


class PersonaUpdateView(MessageMixin, PermissionRequiredMixin, LoggerUpdatedMixin, UpdateView):
    model = Persona
    form_class = PersonaForm
    permission_required = "personas.change_persona"
    raise_exception = True
    mensaje_log = "Actualización de Persona"
    mensaje_exito = "Persona actualizado correctamente"


class PersonaListView(PermissionRequiredMixin, LoggerViewMixin, DatatablesListView):
    model = Persona
    template_name = "personas/persona_list.html"
    permission_required = "personas.list_persona"
    raise_exception = True
    conditional_show_options_permission = "personas.change_persona"
    column_names_and_defs = ['nombres', 'apellidos', 'Tipo de identificación', 'Número de identificación',
                             'Fecha de nacimiento', 'Lugar de nacimiento', 'sexo', 'nacionalidad', 'Estatura en cm',
                             'Peso en kg', 'Dirección de residencia', 'telefono_fijo', 'telefono_celular',
                             'Correo electrónico', 'Fecha de registro', 'Fecha última actualización', 'Estado']
    fields = ['nombres', 'apellidos', 'tipo_id', 'identificacion', 'fecha_nacimiento', 'lugar_nacimiento', 'sexo',
              'nacionalidad', 'estatura', 'peso', 'direccion_residencia', 'telefono_fijo', 'telefono_celular',
              'correo_electronico', 'fecha_registro', 'fecha_update', 'estado']
    options_list = [
        {
            'label_opcion': 'Ver más',
            'url_opcion': 'personas:ver_persona',
            'parametros_url': ['id'],
            'permissions': ['personas.view_persona'],
            'icono': 'fa-eye text-primary'
        },
        {
            'label_opcion': 'Editar',
            'url_opcion': 'personas:editar_persona',
            'parametros_url': ['id'],
            'permissions': ['personas.change_persona'],
            'icono': 'fa-edit text-success',
            'conditions': [
                {
                    'campo': 'estado',
                    'valores_verificar': True,
                    'lambda_evaluacion': lambda x, y: operator.eq(x, y)
                }
            ]
        },
        {
            'label_opcion': 'Eliminar',
            'url_opcion': 'personas:eliminar_persona',
            'parametros_url': ['id'],
            'permissions': ['personas.delete_persona'],
            'confirm_modal': "modal-eliminar",
            'icono': 'fa-trash text-danger'
        },
        {
            'label_opcion': 'Cambiar Estado',
            'url_opcion': 'personas:cambiar_estado_persona',
            'parametros_url': ['id'],
            'permissions': ['personas.change_persona'],
            'confirm_modal': "modal-desactivate",
            'icono': 'fa-ban text-danger'
        }
    ]

    def get_rendered_html_value(self, field, value):
        self.html_value = super(PersonaListView, self).get_rendered_html_value(field, value)
        if field.name == 'estado':
            if value:
                self.html_value = '<label class="label label-primary">ACTIVO</label>'
            else:
                self.html_value = '<label class="label label-danger">INACTIVO</label>'
        return self.html_value


class PersonaCambioEstadoView(MessageMixin, PermissionRequiredMixin, LoggerGetMixin, View):
    permission_required = 'personas.change_persona'
    model = Persona
    mensaje_log = "Cambio de estado de Persona"
    redirect_url = 'personas:listar_persona'
    mensaje_exito = "El estado del persona se ha actualizado correctamente"
    raise_exception = True

    def get(self, request, *args, **kwargs):
        self.object = get_object_or_404(self.model, pk=kwargs['pk'])
        self.object.estado = not self.object.estado
        self.object.save()
        messages.success(self.request, self.mensaje_exito)
        return super(PersonaCambioEstadoView, self).get(request, *args, **kwargs)


class PersonaDetailView(PermissionRequiredMixin, LoggerViewMixin, DetailView):
    model = Persona
    permission_required = "personas.view_persona"
    raise_exception = True


class PersonaDeleteView(PermissionRequiredMixin, GetToPostMixin, LoggerDeleteMixin, DeleteView):
    model = Persona
    permission_required = "personas.delete_persona"
    success_url = reverse_lazy('personas:listar_persona')
    redirect_url = 'personas:listar_persona'
    raise_exception = True
    mensaje_exito = "persona eliminado correctamente"
