from django.conf.urls import url

from .views import (PerfilUsuarioCreateView, PerfilUsuarioUpdateView, PerfilUsuarioListView, RolCreateView, RolListView,
                    PerfilUsuarioCambioEstadoView, RolUpdateView, ExportarDatosView, CargarDatosView,
                    PerfilUsuarioDetailView, PerfilUsuarioDeleteView, EditarPerfilUpdateView)

urlpatterns = [
    url(r'crear-usuario$', PerfilUsuarioCreateView.as_view(), name='crear_usuario'),
    url(r'ver-usuario/(?P<pk>\d+)$', PerfilUsuarioDetailView.as_view(), name='ver_usuario'),
    url(r'editar-usuario/(?P<pk>\d+)/$', PerfilUsuarioUpdateView.as_view(), name='editar_usuario'),
    url(r'editar-perfil/(?P<pk>\d+)/$', EditarPerfilUpdateView.as_view(), name='editar_perfil'),
    url(r'eliminar-usuario/(?P<pk>\d+)/$', PerfilUsuarioDeleteView.as_view(), name='eliminar_usuario'),
    url(r'listar-usuarios$', PerfilUsuarioListView.as_view(), name='listar_usuarios'),
    url(r'cambio-estado-usuario/(?P<pk>\d+)/$', PerfilUsuarioCambioEstadoView.as_view(), name='cambiar_estado_usuario'),
    url(r'crear-rol$', RolCreateView.as_view(), name='crear_rol'),
    url(r'editar-rol/(?P<pk>\d+)/$', RolUpdateView.as_view(), name='editar_rol'),
    url(r'listar-roles$', RolListView.as_view(), name='listar_roles'),
    url(r'exportar-datos$', ExportarDatosView.as_view(), name='exportar_datos'),
    url(r'cargar-datos$', CargarDatosView.as_view(), name='cargar_datos'),
]
