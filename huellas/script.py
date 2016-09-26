from gestion_usuarios.models import PerfilUsuario
from django.contrib.auth.models import Group, Permission

def init():
    group = Group(name="ADMINISTRADOR")
    group.save()
    group.permissions.add(Permission.objects.get(codename="add_perfilusuario"))
    group.permissions.add(Permission.objects.get(codename="change_perfilusuario"))
    group.permissions.add(Permission.objects.get(codename="delete_perfilusuario"))
    group.permissions.add(Permission.objects.get(codename="list_perfilusuario"))
    group.permissions.add(Permission.objects.get(codename="view_perfilusuario"))
    group.permissions.add(Permission.objects.get(codename="add_group"))
    group.permissions.add(Permission.objects.get(codename="change_group"))
    group.permissions.add(Permission.objects.get(codename="delete_group"))
    group.permissions.add(Permission.objects.get(codename="add_permission"))
    group.permissions.add(Permission.objects.get(codename="change_permission"))
    group.permissions.add(Permission.objects.get(codename="delete_permission"))
    group.permissions.add(Permission.objects.get(codename="change_auditorialog"))
    group.save()
    admin = PerfilUsuario(username="admin", first_name="admin", last_name="admin", password="rady_base!", email="desarrollo2@radyconsultores.com", tipo_id=0, identificacion="000000002", is_staff=True)
    admin.set_password(admin.password)
    admin.save()
    admin.groups.add(group)
    admin.save()

init()

