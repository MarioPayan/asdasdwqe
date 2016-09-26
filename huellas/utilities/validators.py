from django.core.validators import RegexValidator

# Validador de string sólo con dígitos.
validador_digitos = RegexValidator(r'^[0-9]*$', 'El valor debe ser numerico.')