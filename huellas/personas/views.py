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
from django.conf import settings

from .models import Persona
from .forms import PersonaForm

import zipfile


class PersonaCreateView(MessageMixin, PermissionRequiredMixin, LoggerCreatedMixin, CreateView):
    model = Persona
    form_class = PersonaForm
    permission_required = "personas.add_persona"
    raise_exception = True
    mensaje_log = "Creación de Persona"
    mensaje_exito = "Persona creado correctamente"
    print(settings.MEDIA_ROOT)
    
    def form_valid(self, form):
        identificador = str(form.instance.identificacion) + "-" + str(form.instance.tipo_id)
        
        form.instance.left_little_finger = "huellas/" + identificador + "/LeftLittle.jp2"
        form.instance.left_ring_finger = "huellas/" + identificador + "/LeftRingFinger.jp2"
        form.instance.left_middle_finger = "huellas/" + identificador + "/LeftMiddleFinger.jp2"
        form.instance.left_index_finger = "huellas/" + identificador + "/LeftIndexFinger.jp2"
        form.instance.left_thumb_finger = "huellas/" + identificador + "/LeftThumb.jp2"
        form.instance.right_little_finger = "huellas/" + identificador + "/RightLittle.jp2"
        form.instance.right_ring_finger = "huellas/" + identificador + "/RightRingFinger.jp2"
        form.instance.right_middle_finger = "huellas/" + identificador + "/RightMiddleFinger.jp2"
        form.instance.right_index_finger = "huellas/" + identificador + "/RightIndexFinger.jp2"
        form.instance.right_thumb_finger = "huellas/" + identificador + "/RightThumb.jp2"
        
        form.instance.left_little_finger_display = "huellas/" + identificador + "/LeftLittle.jpg"
        form.instance.left_ring_finger_display = "huellas/" + identificador + "/LeftRingFinger.jpg"
        form.instance.left_middle_finger_display = "huellas/" + identificador + "/LeftMiddleFinger.jpg"
        form.instance.left_index_finger_display = "huellas/" + identificador + "/LeftIndexFinger.jpg"
        form.instance.left_thumb_finger_display = "huellas/" + identificador + "/LeftThumb.jpg"
        form.instance.right_little_finger_display = "huellas/" + identificador + "/RightLittle.jpg"
        form.instance.right_ring_finger_display = "huellas/" + identificador + "/RightRingFinger.jpg"
        form.instance.right_middle_finger_display = "huellas/" + identificador + "/RightMiddleFinger.jpg"
        form.instance.right_index_finger_display = "huellas/" + identificador + "/RightIndexFinger.jpg"
        form.instance.right_thumb_finger_display = "huellas/" + identificador + "/RightThumb.jpg"
        
        self.object = form.save()
        
        path_to_extract = settings.MEDIA_ROOT + "/huellas/" + identificador + "/"
        path_to_zip = path_to_extract + "huellas.zip"
        
        with zipfile.ZipFile(path_to_zip) as zip_ref:
            zip_ref.extractall(path_to_extract)
        
        return super(PersonaCreateView, self).form_valid(form)


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
