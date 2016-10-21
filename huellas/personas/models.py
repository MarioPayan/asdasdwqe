from django.db import models
from django.core.urlresolvers import reverse

def zip_path(self, *args):
    folder_name = str(self.identificacion) + "-" + str(self.tipo_id)
    file_name = "huellas.zip"
    url = "huellas/" + folder_name + "/" + file_name
    return url
    

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
    
    zip_file = models.FileField(upload_to=zip_path, null=True, blank=True)
    
    left_little_finger = models.ImageField(null=True, blank=True, default="huellas/missing.jpg")
    left_ring_finger = models.ImageField(null=True, blank=True, default="huellas/missing.jpg")
    left_middle_finger = models.ImageField(null=True, blank=True, default="huellas/missing.jpg")
    left_index_finger = models.ImageField(null=True, blank=True, default="huellas/missing.jpg")
    left_thumb_finger = models.ImageField(null=True, blank=True, default="huellas/missing.jpg")
    right_little_finger = models.ImageField(null=True, blank=True, default="huellas/missing.jpg")
    right_ring_finger = models.ImageField(null=True, blank=True, default="huellas/missing.jpg")
    right_middle_finger = models.ImageField(null=True, blank=True, default="huellas/missing.jpg")
    right_index_finger = models.ImageField(null=True, blank=True, default="huellas/missing.jpg")
    right_thumb_finger = models.ImageField(null=True, blank=True, default="huellas/missing.jpg")
    
    left_little_finger_display = models.ImageField(null=True, blank=True, default="huellas/missing.jpg")
    left_ring_finger_display = models.ImageField(null=True, blank=True, default="huellas/missing.jpg")
    left_middle_finger_display = models.ImageField(null=True, blank=True, default="huellas/missing.jpg")
    left_index_finger_display = models.ImageField(null=True, blank=True, default="huellas/missing.jpg")
    left_thumb_finger_display = models.ImageField(null=True, blank=True, default="huellas/missing.jpg")
    right_little_finger_display = models.ImageField(null=True, blank=True, default="huellas/missing.jpg")
    right_ring_finger_display = models.ImageField(null=True, blank=True, default="huellas/missing.jpg")
    right_middle_finger_display = models.ImageField(null=True, blank=True, default="huellas/missing.jpg")
    right_index_finger_display = models.ImageField(null=True, blank=True, default="huellas/missing.jpg")
    right_thumb_finger_display = models.ImageField(null=True, blank=True, default="huellas/missing.jpg")

    def get_absolute_url(self):
        return reverse('personas:listar_persona')

    def __str__(self):
        return str(self.nombres)
        
    def left_little_finger_display_url(self):
        if not self.left_little_finger_display:
            return settings.MEDIA_URL + "fotos_usuario/user.png"
        else:
            return self.left_little_finger_display.url

    class Meta:
        permissions = (
            ('view_persona', 'Permite ver persona'),
            ('list_persona', 'Permite listar persona')
        )
        unique_together = ('tipo_id', 'identificacion')
