import operator
from datetime import datetime
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.models import Group
from django.views.generic import CreateView, UpdateView, View, DetailView, DeleteView
from django.shortcuts import get_object_or_404, redirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib import messages

from utilities.datatables_tools.datatables_tools import DatatablesListView
from .mixins import SuccessRolMixin
from .models import PerfilUsuario
from .forms import RolCreateForm, PerfilUsuarioCreateForm, PerfilUsuarioUpdateForm, EditarPerfilForm
from auditoria.loggers import LoggerCreatedMixin, LoggerUpdatedMixin, LoggerGetMixin, LoggerViewMixin
from utilities.mixins import MessageMixin, GetToPostMixin


class PerfilUsuarioCreateView(MessageMixin, PermissionRequiredMixin, LoggerCreatedMixin, CreateView):
    """
        Autor: RADY CONSULTORES
        Fecha: 2 Septiembre 2016
        Vista de creación de usuarios con permisos, mixin de mensaje para registro exitoso, mixin de auditoría y método
        form_valid para asignar el password al usuario que se está creando
    """

    model = PerfilUsuario
    permission_required = "gestion_usuarios.add_perfilusuario"
    raise_exception = True
    form_class = PerfilUsuarioCreateForm
    mensaje_log = "Creación de usuario"
    mensaje_exito = "Usuario creado correctamente"

    def form_valid(self, form):
        form.instance.set_password(form.instance.password)
        return super(PerfilUsuarioCreateView, self).form_valid(form)


class EditarPerfilUpdateView(MessageMixin, LoginRequiredMixin, UserPassesTestMixin, LoggerUpdatedMixin, UpdateView):
    """
        Autor: RADY CONSULTORES
        Fecha: 16 Septiembre 2016
        Vista para que un usuario edite su propio perfil, esta no incluye permisos sino que utiliza el
        LoginRequiredMixin. Por otro lado se verifica que un usuario no pueda editar a otros usuarios.
    """

    model = PerfilUsuario
    form_class = EditarPerfilForm
    raise_exception = True
    template_name = 'gestion_usuarios/editar_perfil.html'
    mensaje_log = "Actualización de perfil"
    mensaje_exito = "Perfil actualizado correctamente"

    def test_func(self):
        """
            Autor: RADY CONSULTORES
            Fecha: 2 Septiembre 2016
            Método para el UserPassesTestMixin que verifica si se un usuario se está editando a si mismo, si no se
            cumple alguna de las dos, no se le deja ingresar a la vista
        """

        editar = False
        usuario_actual = int(self.request.user.id)
        usuario_editar = int(self.request.resolver_match.kwargs['pk'])

        if usuario_actual == usuario_editar:
            editar = True
        return editar

    def get_success_url(self):
        return reverse('inicio')


class PerfilUsuarioUpdateView(MessageMixin, PermissionRequiredMixin, LoggerUpdatedMixin, UpdateView):
    """
        Autor: RADY CONSULTORES
        Fecha: 2 Septiembre 2016
        Vista de actualización de usuarios con permisos, mixin de mensaje para actualización exitosa, mixin de auditoría
        mixin de test y método form_valid para asignar el password al usuario que se está creando
    """

    model = PerfilUsuario
    form_class = PerfilUsuarioUpdateForm
    permission_required = 'gestion_usuarios.change_perfilusuario'
    raise_exception = True
    mensaje_log = "Actualización de usuario"
    mensaje_exito = "Usuario actualizado correctamente"

    def get_success_url(self):
        return reverse('gestion_usuarios:listar_usuarios')

    def get(self, request, *args, **kwargs):
        """
            Autor: RADY CONSULTORES
            Fecha: 2 Septiembre 2016
            Se aprovecha el método get para validar que el usuario que se está tratando de editar esté activo
        """

        usuario = get_object_or_404(PerfilUsuario, pk=kwargs['pk'])
        if not usuario.is_active:
            return redirect(usuario.get_absolute_url())
        else:
            return super(PerfilUsuarioUpdateView, self).get(self.request, *args, **kwargs)


class PerfilUsuarioListView(PermissionRequiredMixin, LoggerViewMixin, DatatablesListView):
    """
        Autor: RADY CONSULTORES
        Fecha: 2 Septiembre 2016
        Vista para listar usuarios utilizando el DatatablesListView, se configuran todos sus parámetros tales como
        permisos, nombre del template a usar, campos, definición de nombres de columnas y lista de opciones para cada
        uno de los registros de la tabla con sus respectivas configuraciones
    """

    model = PerfilUsuario
    template_name = "gestion_usuarios/perfilusuario_list.html"
    permission_required = "gestion_usuarios.change_perfilusuario"
    raise_exception = True
    fields = ["username", "tipo_id", "identificacion", "first_name", "last_name", "last_login",
              "groups", "is_active"]
    column_names_and_defs = ["Nombre de Usuario", "Tipo ID", "N° Identificación", "Nombres", "Apellidos",
                             "Último Inicio de Sesión", "Roles", "Estado"]
    options_list = [
        {
            'label_opcion': 'Ver más',
            'url_opcion': 'gestion_usuarios:ver_usuario',
            'parametros_url': ['id'],
            'permissions': ['gestion_usuarios.view_perfilusuario'],
            'icono': 'fa-eye',
        },
        {
            'label_opcion': 'Editar',
            'url_opcion': 'gestion_usuarios:editar_usuario',
            'parametros_url': ['id'],
            'permissions': ['gestion_usuarios.add_perfilusuario'],
            'icono': 'fa-edit',
            'conditions': [
                {
                    'campo': 'is_active',
                    'valores_verificar': True,
                    'lambda_evaluacion': lambda x, y: operator.eq(x, y)
                }
            ]
        },
        {
            'label_opcion': 'Eliminar',
            'url_opcion': 'gestion_usuarios:eliminar_usuario',
            'parametros_url': ['id'],
            'permissions': ['gestion_usuarios.delete_perfilusuario'],
            'confirm_modal': "modal-eliminar",
            'icono': 'fa-trash text-danger',
        },
        {
            'label_opcion': 'Cambiar estado',
            'url_opcion': 'gestion_usuarios:cambiar_estado_usuario',
            'parametros_url': ['id'],
            'permissions': ['gestion_usuarios.add_perfilusuario'],
            'confirm_modal': "modal-desactivate",
            'icono': 'fa-ban text-danger',
        }
    ]

    def get_rendered_html_value(self, field, value):
        """
            Autor: RADY CONSULTORES
            Fecha: 2 Septiembre 2016
            Método mediante el cual se solicita a la vista que pinte los campos last_login con una descripción clara
            y el estado del usuario con labels de colores según su estado actual
        """

        self.html_value = super(PerfilUsuarioListView, self).get_rendered_html_value(field, value)

        if field.name == "last_login":
            if value is None:
                self.html_value = "Nunca"
            else:
                self.html_value = datetime.strftime(value, "%y-%m-%d %H:%M")
        if field.name == 'is_active':
            if value:
                self.html_value = '<label class="label label-primary">ACTIVO</label>'
            else:
                self.html_value = '<label class="label label-danger">INACTIVO</label>'
        return self.html_value


class PerfilUsuarioCambioEstadoView(MessageMixin, PermissionRequiredMixin, LoggerGetMixin, View):
    """
        Autor: RADY CONSULTORES
        Fecha: 2 Septiembre 2016
        Vista de cambio de estado con mensajes, permisos y auditoría
    """

    permission_required = 'gestion_usuarios.add_perfilusuario'
    raise_exception = True
    model = PerfilUsuario
    mensaje_log = "Cambio de estado de usuario"
    redirect_url = 'gestion_usuarios:listar_usuarios'

    def get(self, request, *args, **kwargs):
        """
            Autor: RADY CONSULTORES
            Fecha: 2 Septiembre 2016
            El cambio de estado se realiza en el método get
        """

        self.object = get_object_or_404(PerfilUsuario, pk=kwargs['pk'])
        self.object.is_active = not self.object.is_active
        self.object.save()
        messages.success(self.request, 'Usuario ' + self.object.get_estado_accion() + ' correctamente')
        return super(PerfilUsuarioCambioEstadoView, self).get(request, *args, **kwargs)


class PerfilUsuarioDetailView(PermissionRequiredMixin, LoggerViewMixin, DetailView):
    """
        Autor: RADY CONSULTORES
        Fecha: 2 Septiembre 2016
        Vista para el ver detalle de los usuarios, con permisos.
    """

    model = PerfilUsuario
    permission_required = "gestion_usuarios.view_perfilusuario"
    raise_exception = True


class PerfilUsuarioDeleteView(PermissionRequiredMixin, GetToPostMixin, LoggerGetMixin, DeleteView):
    """
        Autor: RADY CONSULTORES
        Fecha: 2 Septiembre 2016
        Vista para eliminar usuarios, con permisos, auditoria y un mixin que redirecciona de get a post para no tener
        necesidad de utilizar un template intermedio de confirmación
    """

    model = PerfilUsuario
    permission_required = "gestion_usuarios.delete_perfilusuario"
    mensaje_log = "Eliminación de usuario"
    success_url = reverse_lazy('gestion_usuarios:listar_usuarios')
    redirect_url = 'gestion_usuarios:listar_usuarios'
    raise_exception = True


class RolCreateView(MessageMixin, PermissionRequiredMixin, LoggerCreatedMixin, SuccessRolMixin, CreateView):
    """
        Autor: RADY CONSULTORES
        Fecha: 2 Septiembre 2016
        Vista para crear roles con permisos, auditoria y un mixin que obtiene el success url para los roles
    """

    model = Group
    permission_required = "auth.add_group"
    raise_exception = True
    form_class = RolCreateForm
    template_name = "gestion_usuarios/rol_form.html"
    mensaje_log = "Creación de Rol"
    mensaje_exito = "Rol creado correctamente"


class RolUpdateView(MessageMixin, PermissionRequiredMixin, LoggerUpdatedMixin, SuccessRolMixin, UpdateView):
    """
        Autor: RADY CONSULTORES
        Fecha: 2 Septiembre 2016
        Vista para editar roles con permisos, auditoria y un mixin que obtiene el success url para los roles
    """

    model = Group
    permission_required = "auth.change_group"
    raise_exception = True
    form_class = RolCreateForm
    template_name = "gestion_usuarios/rol_form.html"
    mensaje_log = "Actualización de Rol"
    mensaje_exito = "Rol actualizado correctamente"


class RolListView(PermissionRequiredMixin, LoggerViewMixin, DatatablesListView):
    """
        Autor: RADY CONSULTORES
        Fecha: 2 Septiembre 2016
        Vista para listar roles con DatatablesMixin, permisos y opción de editar rol.
    """

    model = Group
    template_name = "gestion_usuarios/rol_list.html"
    permission_required = "auth.change_group"
    raise_exception = True
    fields = ["name", "permissions"]
    column_names_and_defs = ["Nombre del Rol", "Permisos"]
    options_list = [
        {
            'label_opcion': 'Editar',
            'url_opcion': 'gestion_usuarios:editar_rol',
            'parametros_url': ['id'],
            'permissions': ['auth.change_group'],
            'icono': 'fa-edit'
        }
    ]


class CargarDatosView(View):
    """
        Autor: RADY CONSULTORES
        Fecha: 2 Septiembre 2016
        Vista para cargar toda la información sobre los roles a partir de un archivo generado por la vista
        ExportarDatosView, en esta se utiliza el comando loaddata de django
    """

    def get(self, request, *args, **kwargs):
        """
            Autor: RADY CONSULTORES
            Fecha: 2 Septiembre 2016
            En el método get se llama el comando para cargar los datos desde el archivo roles.json generado desde el
            sistema
        """

        from django.core.management import call_command
        call_command('loaddata', 'datos_iniciales/roles.json', verbosity=0)
        messages.success(request, "Datos cargados correctamente")
        return redirect('gestion_usuarios:listar_roles')


class ExportarDatosView(View):
    """
        Autor: RADY CONSULTORES
        Fecha: 2 Septiembre 2016
        Vista para exportar datos sobre los roles para poder reutilizarla en las diferentes instancias del proyecto
        en esta se utiliza el comando dumpdata para exportar el archivo roles.json
    """

    def get(self, request, *args, **kwargs):
        """
            Autor: RADY CONSULTORES
            Fecha: 2 Septiembre 2016
            Método en el cual se lleva a cabo toda la acción
        """

        from django.core.management import call_command
        call_command('dumpdata', 'auth.group', output="datos_iniciales/roles.json")
        messages.success(request,
                         "Se ha exportado la información de los roles en el archivo 'datos_iniciales/roles.json'")
        return redirect('gestion_usuarios:listar_roles')
