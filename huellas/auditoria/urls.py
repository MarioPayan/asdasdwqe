from django.conf.urls import url
from .views import AuditoriaListView, AuditoriaDeleteView, AuditoriaDetailView

urlpatterns = [
    url(r'^listar$', AuditoriaListView.as_view(), name='listar'),
    url(r'^eliminar/(?P<pk>\d+)/$', AuditoriaDeleteView.as_view(), name='eliminar'),
    url(r'^detalle/(?P<pk>\d+)/$', AuditoriaDetailView.as_view(), name='detalle'),
]
