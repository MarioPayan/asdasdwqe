from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache


class MessageMixin(object):
    """
        Autor: RADY CONSULTORES
        Fecha: 2 Septiembre 2016
        Mixin para mostrar mensajes de exito o de error dependiendo la necesidad, se utiliza el framework de mensajes
        de Django y se utiliza el plugin toastr para mostrarlo desde el template
    """

    # Mensajes por defecto
    mensaje_exito = "¡La información se ha guardo exitosamente!"
    mensaje_error = "El formulario tiene errores, por favor revise la información."

    def form_valid(self, form):
        messages.success(self.request, self.mensaje_exito)
        return super(MessageMixin, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, self.mensaje_error)
        return super(MessageMixin, self).form_invalid(form)


class GetToPostMixin(object):
    """
        Autor: RADY CONSULTORES
        Fecha: 2 Septiembre 2016
        Mixin que redirecciona desde el método get al método post, se utiliza en las vistas delete para evitar
        el uso del template confirm_delete
    """

    def get(self, request, *args, **kwargs):
        super(GetToPostMixin, self).get(request, *args, **kwargs)
        return self.post(request, *args, **kwargs)