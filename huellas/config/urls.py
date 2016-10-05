from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(template_name="base.html"), name="inicio"),
    url(r'^login$', auth_views.login, name='login'),
    url(r'^logout$', auth_views.logout, {'next_page': 'inicio'}, name='logout'),
    url(r'^password-reset/', auth_views.password_reset,  name='password_reset'),
    url(r'^password-reset-done/', auth_views.password_reset_done,  name='password_reset_done'),
    url(r'^password-reset-confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm,  name='password_reset_confirm'),
    url(r'^password-reset-complete/', auth_views.password_reset_complete,  name='password_reset_complete'),
    url(r'^password-change/', auth_views.password_change,  name='password_change'),
    url(r'^password-change-done/', auth_views.password_change_done,  name='password_change_done'),
    url(r'^usuarios/', include('gestion_usuarios.urls', namespace='gestion_usuarios')),
    url(r'^auditoria/', include('auditoria.urls', namespace='auditoria')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    url(r'^personas/', include('personas.urls', namespace='personas')),
]