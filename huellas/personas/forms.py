from .models import Persona
from django import forms
from utilities.widgets import MyDateWidget


class PersonaForm(forms.ModelForm):
    required_css_class = 'required'
    letras_validation = {
        'data-fv-regexp-regexp': '/^[a-zA-Z\s]*$/',
        'data-fv-regexp': "true"
    }
    minymax_estatura_peso = {
        'min': 1,
        'max': 999
    }
    length_telefonos = {
        'minlength': 7,
        'maxlength': 15
    }

    def __init__(self, *args, **kwargs):
        super(PersonaForm, self).__init__(*args, **kwargs)
        self.fields['fecha_nacimiento'].widget = MyDateWidget()
        self.fields['nombres'].widget.attrs.update(self.letras_validation)
        self.fields['apellidos'].widget.attrs.update(self.letras_validation)
        self.fields['identificacion'].widget.attrs.update({
            'min': 0,
            'maxlength': 15,
        })
        self.fields['estatura'].widget.attrs.update(self.minymax_estatura_peso)
        self.fields['telefono_fijo'].widget.attrs.update(self.length_telefonos)
        self.fields['telefono_celular'].widget.attrs.update(self.length_telefonos)

    class Meta:
        model = Persona
        fields = ['nombres', 'apellidos', 'tipo_id', 'identificacion', 'fecha_nacimiento', 'lugar_nacimiento', 'sexo',
                  'nacionalidad', 'estatura', 'peso', 'direccion_residencia', 'telefono_fijo', 'telefono_celular',
                  'correo_electronico']
