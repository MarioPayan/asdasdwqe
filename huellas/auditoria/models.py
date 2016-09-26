from django.db import models
from django.conf import settings

from gestion_usuarios.models import PerfilUsuario


class AuditoriaLog(models.Model):
    accion = models.TextField()
    usuario = models.CharField(max_length=150)
    tipo_usuario = models.CharField(max_length=150)
    fecha_log = models.DateField('timestamp', auto_now=True)
    hora_log = models.TimeField('timestamp', auto_now=True)
    ip_cliente = models.CharField(max_length=50)
    old = models.CharField(blank=True, max_length=500)
    new = models.CharField(blank=True, max_length=500)
    log_level = models.IntegerField()

    def log(self, request, msg, old=None, new=None):
        self.accion = msg
        usuario = PerfilUsuario.objects.get(id=request.user.id)
        self.usuario = usuario.username
        try:
            tipo = usuario.groups.all()[0]
            self.tipo_usuario = tipo
        except IndexError:
            self.tipo_usuario = "NO ESPECIFICADO"
        self.ip_cliente = get_client_ip(request)

        if old and new:
            self.old = ','.join('{}:{}'.format(key, val) for key, val in old.items())
            self.new = ','.join('{}:{}'.format(key, val) for key, val in new.items())
        self.log_level = settings.LOG_LEVEL
        self.save()


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
