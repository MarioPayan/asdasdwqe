from django import forms
from django.contrib.auth.models import Group

from .models import PerfilUsuario


class PerfilUsuarioCreateForm(forms.ModelForm):

    """
        Autor: RADY CONSULTORES
        Fecha: 2 Septiembre 2016
        Formulario de creación para los usuarios, en este se incluye un campo de confirmación de contraseña,
        el asterisco para campos requeridos y widgets para campos
    """

    confirmar_pass = forms.CharField(required=True,
                                     widget=forms.PasswordInput(attrs={'placeholder':
                                                                       'Por favor repita su contraseña...'}),
                                     label="Confirmar contraseña")
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        """
            Autor: RADY CONSULTORES
            Fecha: 2 Septiembre 2016
            Método constructor en donde se asignan las propiedades de los campos, widgets, entre otros.
        """

        super(PerfilUsuarioCreateForm, self).__init__(*args, **kwargs)
        if self.instance.pk is None:
            self.fields['password'].widget = forms.PasswordInput()
        self.fields['groups'].widget.attrs.update({'class': 'one form-control'})
        self.fields['confirmar_pass'].widget.attrs.update({
                    'data-fv-identical-field': 'password',
                    'data-fv-identical': "true"
                })
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

    def clean(self):
        """
            Autor: RADY CONSULTORES
            Fecha: 2 Septiembre 2016
            Método clean utilizado para validar del lado del servidor que las dos contraseñas sean iguales
        """
        cleaned_data = super(PerfilUsuarioCreateForm, self).clean()
        password = cleaned_data.get("password")
        confirmar_password = cleaned_data.get("confirmar_pass")

        if self.instance.pk is None:
            if confirmar_password != password:
                msg = "La contraseña no es igual a la de confirmación"
                self.add_error("confirmar_pass", msg)

        return cleaned_data

    class Meta:
        model = PerfilUsuario
        fields = ['first_name', 'last_name', 'username', 'password', 'tipo_id', 'identificacion', 'email', 'foto',
                  'groups']


class PerfilUsuarioUpdateForm(PerfilUsuarioCreateForm):

    """
        Autor: RADY CONSULTORES
        Fecha: 2 Septiembre 2016
        Formulario de actualización que hereda del formulario de creación y sobreescribe sus propiedades
    """

    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super(PerfilUsuarioUpdateForm, self).__init__(*args, **kwargs)
        self.fields['tipo_id'].widget.attrs['readonly'] = True
        self.fields['tipo_id'].widget.attrs.update({'style': 'pointer-events: none;'})
        self.fields['identificacion'].widget.attrs['readonly'] = True
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['confirmar_pass'].required = False

    # Métodos clean por campo utilizados para evitar inyección de contenido mediante javascript al editar campos
    # que no son editables
    def clean_identificacion(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.identificacion
        else:
            return self.cleaned_data['identificacion']

    def clean_tipo_id(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.tipo_id
        else:
            return self.cleaned_data['tipo_id']

    def clean_username(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.username
        else:
            return self.cleaned_data['username']

    class Meta(PerfilUsuarioCreateForm.Meta):
        fields = ['first_name', 'last_name', 'username', 'tipo_id', 'identificacion', 'email', 'foto', 'groups']


class RolCreateForm(forms.ModelForm):

    """
        Autor: RADY CONSULTORES
        Fecha: 2 Septiembre 2016
        Formulario de creación de roles con plugin para permisos y asterisco en campos obligatorios
    """

    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super(RolCreateForm, self).__init__(*args, **kwargs)
        self.fields['permissions'].widget.attrs.update({'class': 'chosen form-control',
                                                        'data-placeholder': "Escoja los permisos..."})

    class Meta:
        model = Group
        fields = ['name', 'permissions']


class EditarPerfilForm(forms.ModelForm):
    """
        Autor: RADY CONSULTORES
        Fecha: 16 Septiembre 2016
        Formulario para que un usuario edite su propio perfil
    """

    def __init__(self, *args, **kwargs):
        super(EditarPerfilForm, self).__init__(*args, **kwargs)

    class Meta:
        model = PerfilUsuario
        fields = ['foto', 'first_name', 'last_name', 'email']
