from django.conf.urls import url

from .views import (PersonaCreateView, PersonaUpdateView, PersonaListView,
                    PersonaCambioEstadoView, PersonaDetailView, PersonaDeleteView)

urlpatterns = [
    url(r'^crear-persona$', PersonaCreateView.as_view(), name='crear_persona'),
    url(r'^editar-persona/(?P<pk>\d+)/$', PersonaUpdateView.as_view(), name='editar_persona'),
    url(r'^cambiar-estado-persona/(?P<pk>\d+)/$', PersonaCambioEstadoView.as_view(), name='cambiar_estado_persona'),
    url(r'^listar-persona$', PersonaListView.as_view(), name='listar_persona'),
    url(r'^ver-persona/(?P<pk>\d+)$', PersonaDetailView.as_view(), name='ver_persona'),
    url(r'^eliminar-persona/(?P<pk>\d+)$', PersonaDeleteView.as_view(), name='eliminar_persona')
]
