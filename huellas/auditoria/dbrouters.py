class LogRouter(object):
    """
    A router to control all database operations on models in the
    auditoria application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read AuditoriaLog models go to logs.
        """
        if model._meta.app_label == 'auditoria':
            return 'logs'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write AuditoriaLog models go to logs.
        """
        if model._meta.app_label == 'auditoria':
            return 'logs'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the AuditoriaLog app is involved.
        """
        if obj1._meta.app_label == 'auditoria' or obj2._meta.app_label == 'auditoria':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auditoria app only appears in the 'logs'
        database.
        """
        if app_label == 'auditoria':
            return db == 'logs'
        return None
