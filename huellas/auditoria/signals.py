from django.conf import settings
from django.contrib.auth.signals import user_logged_in, user_logged_out  # , user_login_failed

from .models import AuditoriaLog


def log_login(sender, user, request, **kwargs):
    """
    Autor: RADY CONSULTORES
    Fecha: 18 Septiembre 2016
    Método que guarda el log en el sistema cuando un usuario inicia sesión. Se usan las señales de django.

    :param sender: Clase que envía la señar
    :param user: Instancia de usuario que inicia sesión
    :param request: HttpRequest
    :param kwargs: Argumentos adicionales pasados al método
    :return: void
    """
    logger = AuditoriaLog()
    logger.log(request, "Inicio de sesión en el sistema" + ": " + user.__str__())


def log_logout(sender, user, request, **kwargs):
    """
    Autor: RADY CONSULTORES
    Fecha: 18 Septiembre 2016
    Método que guarda el log en el sistema cuando un usuario cierra sesión. Se usan las señales de django.

    :param sender: Clase que envía la señar
    :param user: Instancia de usuario que cierra sesión
    :param request: HttpRequest
    :param kwargs: Argumentos adicionales pasados al método
    :return: void
    """
    logger = AuditoriaLog()
    logger.log(request, "Cerrado de sesión en el sistema" + ": " + user.__str__())


def connect_signals():
    """
    Autor: RADY CONSULTORES
    Fecha: 18 Septiembre 2016
    Método usado para conectar las señales de sesión con sus manejadores correspondientes.

    :return: void
    """
    if settings.LOG_LEVEL == 3:
        user_logged_in.connect(log_login)
        user_logged_out.connect(log_logout)
    """
    Esta conexión no se puede hacer ya que el request ha sido implementado en la versión de desarrollo de django.
    Se deja en stand by para un futuro uso

    user_login_failed.connect(log_login_failed)
    """

"""
def log_login_failed(sender, credentials, request, **kwargs):
    # Método para uso futuro cuando el login falle

    logger = AuditoriaLog()
    logger.log(request, "Inicio de sesión fallida" + ": " + credentials['username'])
"""