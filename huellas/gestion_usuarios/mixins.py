from django.core.urlresolvers import reverse


class SuccessRolMixin(object):

    def get_success_url(self):
        return reverse('gestion_usuarios:listar_roles')