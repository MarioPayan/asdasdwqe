from django.db import models
from django.core.urlresolvers import reverse


class Persona(models.Model):
    tipo_id_choices = (
        (0, "CÉDULA DE CIUDADANÍA"),
        (1, "TARJETA DE IDENTIDAD"),
        (2, "CÉDULA DE EXTRANJERO"),
        (3, "PASAPORTE"),
    )

    sexo_choices = (
        (0, "MASCULINO"),
        (1, "FEMENINO"),
    )

    nombres = models.CharField(max_length=30)
    apellidos = models.CharField(max_length=30)
    tipo_id = models.IntegerField(verbose_name="Tipo de identificación", choices=tipo_id_choices)
    identificacion = models.IntegerField(verbose_name="Número de identificación")
    fecha_nacimiento = models.DateField(verbose_name="Fecha de nacimiento")
    lugar_nacimiento = models.CharField(verbose_name="Lugar de nacimiento", max_length=40)
    sexo = models.IntegerField(choices=sexo_choices)
    nacionalidad = models.CharField(max_length=40)
    estatura = models.IntegerField(verbose_name="Estatura en cm")
    peso = models.IntegerField(verbose_name="Peso en kg")
    direccion_residencia = models.CharField(verbose_name="Dirección de residencia", max_length=80)
    telefono_fijo = models.IntegerField()
    telefono_celular = models.IntegerField()
    correo_electronico = models.EmailField(verbose_name="Correo electrónico")
    fecha_registro = models.DateField(verbose_name="Fecha de registro", auto_now_add=True)
    fecha_update = models.DateField(verbose_name="Fecha última actualización", auto_now=True)
    estado = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('personas:listar_persona')

    def __str__(self):
        return str(self.nombres)

    class Meta:
        permissions = (
            ('view_persona', 'Permite ver persona'),
            ('list_persona', 'Permite listar persona')
        )
        unique_together = ('tipo_id', 'identificacion')
