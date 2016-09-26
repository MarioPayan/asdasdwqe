from django.views.generic import DeleteView, DetailView
from django.core.urlresolvers import reverse
from django.contrib.auth.mixins import PermissionRequiredMixin

from .models import AuditoriaLog
from utilities.datatables_tools.datatables_tools import DatatablesListView


class AuditoriaListView(PermissionRequiredMixin, DatatablesListView):
    """
    Autor: RADY CONSULTORES
    Fecha: 25 Septiembre 2016
    Vista para listar las acciones recientes en el sistema.
    """
    model = AuditoriaLog
    template_name = 'auditoria/auditorialog_list.html'
    permission_required = 'auditoria.change_auditorialog'
    raise_exception = True
    fields = ['accion', 'fecha_log', 'hora_log', 'ip_cliente', 'tipo_usuario', 'usuario', 'log_level']
    column_names_and_defs = [{'title': 'Acción Sobre el Sistema', 'className': 'capfirst'},
                             'Fecha', 'Hora', 'Ip Usuario', 'Tipo de usuario', 'Usuario', 'Nivel Log']
    options_list = [
        {
            'label_opcion': 'Ver más',
            'url_opcion': 'auditoria:detalle',
            'parametros_url': ['id'],
            'icono': 'fa-eye',
            'conditions': [
                {
                    'campo': 'new',
                    'valores_verificar': '',
                    'lambda_evaluacion': lambda x, y: x is not y
                }
            ]
        },
        {
            'label_opcion': 'Eliminar Registro',
            'url_opcion': 'auditoria:eliminar',
            'parametros_url': ['id'],
            'confirm_modal': False,
            'icono': 'fa-trash'
        }
    ]


class AuditoriaDeleteView(PermissionRequiredMixin, DeleteView):
    """
    Autor: RADY CONSULTORES
    Fecha: 25 Septiembre 2016
    Vista para borrar acciones recientes en el sistema
    """
    model = AuditoriaLog
    permission_required = 'auditoria.change_auditorialog'
    mensaje_log = "Eliminación de registro"

    def get_success_url(self):
        return reverse("auditoria:listar")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class AuditoriaDetailView(PermissionRequiredMixin, DetailView):
    """
    Autor: RADY CONSULTORES
    Fecha: 25 Septiembre 2016
    Esta vista procesa los datos guardados de old y new cuando se modifica un objeto y los deja listo para ser
    usados en la plantilla. Esta vista sólo se usa para las auditorías guardadas con LoggerUpdateView.
    """
    permission_required = 'auditoria.change_auditorialog'
    model = AuditoriaLog

    def get_context_data(self, **kwargs):
        context = super(AuditoriaDetailView, self).get_context_data(**kwargs)
        self.object = self.get_object()
        old = self.object.old.split(',')
        new = self.object.new.split(',')

        context['old'] = old
        context['new'] = new
        return context
