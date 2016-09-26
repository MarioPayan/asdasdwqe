"""
En el settings se debe configurar la variable de estado LOG_LEVEL que determinará a que tantas acciones se le
deben hacer seguimiento en el módulo de auditoría
"""
from django.conf import settings
from django.shortcuts import redirect
from django.forms.models import model_to_dict

from .models import AuditoriaLog


class LoggerCreatedMixin(object):
    """
    Autor: RADY CONSULTORES
    Fecha: 18 Septiembre 2016
    Mixin que guarda un log en el sistema cuando un objeto es creado en la base de datos.
    """
    def form_valid(self, form):
        if settings.LOG_LEVEL != 0:
            logger = AuditoriaLog()
            self.object = form.save(commit=False)
            logger.log(self.request, self.mensaje_log + ": " + self.object.__str__())
        return super(LoggerCreatedMixin, self).form_valid(form)


class LoggerUpdatedMixin(object):
    """
    Autor: RADY CONSULTORES
    Fecha: 18 Septiembre 2016
    Mixin que guarda un log en el sistema cuando un objeto es actualizado en la base de datos. Se guardan los cambios
    por medio de diccionarios en forma de strings, ya que no hay campos json en sqlite.
    """
    old_obj = None
    new_obj = None

    def form_valid(self, form):
        if settings.LOG_LEVEL != 0:
            logger = AuditoriaLog()

            # Este se deja por fuera del 'if' porque se necesita el str para el log
            old_temp_object = self.model.objects.get(id=self.object.id)

            if settings.LOG_LEVEL != 1:
                # Se crea el diccionario de datos del objeto sin actualizar
                self.old_obj = model_to_dict(old_temp_object)

                # Se crea el diccionario de datos del objeto actulizado
                new_temp_obj = form.save(commit=False)
                self.new_obj = model_to_dict(new_temp_obj)

            logger.log(self.request, self.mensaje_log + ": " + old_temp_object.__str__(), self.old_obj, self.new_obj)
        return super(LoggerUpdatedMixin, self).form_valid(form)


class LoggerGetMixin(object):
    """
    Autor: RADY CONSULTORES
    Fecha: 18 Septiembre 2016
    Mixin que guarda un log en el sistema cuando un objeto es actualizado en la base de datos a través del método get.
    Al ser una actualización personalizada, se debe colocar un mensaje claro en el atributo mensaje_log, por ejemplo
    'Cambio de estado'. También se debe especificar el modelo en el atributo model.

    Cuando se obtenga la instancia del objeto a actualizar, esta se debe guardar en self.object para que funcione
    correctamente. También se debe inicializar el atributo redirect_url, el cual es un string con en nombre de la url
    hacia la cual se desea redireccionar al finalizar el guardado del log, además en el método se debe hacer un
    llamado al super de la clase con el método get al final.
    """
    object = None
    redirect_url = None
    model = None

    def get(self, request, *args, **kwargs):
        if settings.LOG_LEVEL != 0:
            logger = AuditoriaLog()
            logger.log(request, self.mensaje_log + " " + self.model.__name__ + ": " + self.object.__str__())
        return redirect(self.redirect_url)


class LoggerViewMixin(object):
    """
    Autor: RADY CONSULTORES
    Fecha: 18 Septiembre 2016
    Mixin que guarda un log en el sistema cuando un usuario accede a una vista que usa este mixin.
    """
    def get(self, request, *args, **kwargs):
        if settings.LOG_LEVEL == 2:
            if not request.is_ajax():
                logger = AuditoriaLog()
                logger.log(request, "Acceso a url: " + request.get_full_path())
        return super(LoggerViewMixin, self).get(request, *args, **kwargs)


class LoggerDeleteMixin(object):
    """
    Autor: RADY CONSULTORES
    Fecha: 18 Septiembre 2016
    Mixin que guarda un log en el sistema cuando un objeto es borrado de la base de datos.
    """
    def delete(self, request, *args, **kwargs):
        if settings.LOG_LEVEL != 0:
            logger = AuditoriaLog()
            logger.log(request, "Objeto borrado de la base de datos: " + self.model.__name__ + ": " +
                       self.object.__str__())
        return super(LoggerDeleteMixin, self).delete(request, *args, **kwargs)
