from gestion_usuarios.models import PerfilUsuario


def perfilusuario_global(request):
    if hasattr(request, 'user'):
        try:
            objeto_usuario = PerfilUsuario.objects.get(id=request.user.id)
        except PerfilUsuario.DoesNotExist:
            return {}

        return {'usuario': objeto_usuario}
    else:
        return {}
