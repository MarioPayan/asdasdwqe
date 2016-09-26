from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.conf import settings

# Create your models here.


class PerfilUsuario(AbstractUser):
    TIPO_IDENTIDAD = (
        (0, 'CÉDULA DE CIUDADANÍA'),
        (1, 'CÉDULA DE EXTRANJERÍA'),
        (2, 'PASAPORTE'),
    )

    TIPO_GENERO = (
        (0, 'MASCULINO'),
        (1, 'FEMENINO'),
        (2, 'OTRO')
    )

    tipo_id = models.IntegerField(verbose_name='Tipo de identificación', choices=TIPO_IDENTIDAD)
    identificacion = models.CharField(max_length=100, verbose_name='Número de identificación', unique=True)
    foto = models.ImageField(upload_to='fotos_usuario/', null=True, blank=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('gestion_usuarios:listar_usuarios')

    def get_estado_accion(self):
        return ('desactivado', 'activado')[self.is_active]

    def get_img_url(self):
        if not self.foto:
            return settings.MEDIA_URL + "fotos_usuario/user.png"
        else:
            return self.foto.url

    class Meta:
        permissions = (
            ('view_perfilusuario', 'Permite ver perfilusuario'),
            ('list_perfilusuario', 'Permite listar perfilusuario')
        )
