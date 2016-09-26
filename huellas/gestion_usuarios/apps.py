from django.apps import AppConfig


class GestionUsuariosConfig(AppConfig):
    name = 'gestion_usuarios'

    def ready(self):
        """
        Autor: RADY CONSULTORES
        Fecha: 18 Septiembre 2016
        Se invoca cuando la aplicación está lista y termina de cargar. Se llama al connect_signals de auditoría aquí,
        ya que ese módulo usa el modelo de esta aplicación y este es el momento correcto de invocar las conexiones.

        :return: void
        """
        from auditoria.signals import connect_signals
        connect_signals()
