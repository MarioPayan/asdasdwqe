from datetimewidget.widgets import DateWidget
from django.forms import SelectMultiple
from django.utils.datastructures import MultiValueDict


def MyDateWidget():
    """
        Autor: RADY CONSULTORES
        Fecha: 2 Septiembre 2016
        Método que retorna un DateWidget del django-datetime-widget para ser utilizado en los formularios
    """

    return DateWidget(usel10n=False, bootstrap_version=3, options={'format': 'yyyy-mm-dd', 'startView': 2, 'language': 'es'})


class ArrayFieldSelectMultiple(SelectMultiple):

    """
        Widget para campos del tipo ArrayField, código fuente de
        https://bradmontgomery.net
        Autor: brad@bradmontgomery.net
    """

    def __init__(self, base_field, *args, **kwargs):

        # Se agrega el atributo base_field para poder validar los campos de acuerdo al tipo establecido en las
        # opciones.
        self.base_field = base_field
        self.delimiter = kwargs.pop("delimiter", ",")
        kwargs['attrs'] = {'class': 'chosen-select'}
        super(ArrayFieldSelectMultiple, self).__init__(*args, **kwargs)

    def value_from_datadict(self, data, files, name):
        if isinstance(data, MultiValueDict):
            return self.delimiter.join(data.getlist(name))
        return data.get(name, None)

    class Media:
        css = {
            'all': ('css/plugins/chosen/chosen.css',)
        }
        js = {'js/plugins/chosen/chosen.jquery.js'}


