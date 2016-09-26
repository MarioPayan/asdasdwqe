"""
    Autor: RADY CONSULTORES
    Fecha: 2 Septiembre 2016
    Archivo de menús para gestión de usuarios utilizando menuware personalizado
"""

MENUWARE_MENU = {
    "LEFT_NAV_MENU": [
        {
            "name": "Gestión usuarios",
            "url": "#",
            "render_for_authenticated": True,
            "render_for_user_when_has_permission": "gestion_usuarios.add_perfilusuario",
            "icon": "fa fa-users",
            "submenu": [  # Show submenu to those who could see the `parent` menu
                {
                    "name": "Usuarios",
                    "url": "gestion_usuarios:listar_usuarios"
                },
                {
                    "name": "Roles",
                    "url": "gestion_usuarios:listar_roles",
                },
            ],
        }
    ]
}