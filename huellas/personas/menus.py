MENUWARE_MENU = {
    "LEFT_NAV_MENU": [
        {
            "name": "Personas",
            "url": "#",
            "render_for_authenticated": True,
            "render_for_user_when_has_permission": "personas.list_persona",
            "icon": "fa fa-group",
            "submenu": [
                {
                    "name": "Persona",
                    "url": "personas:listar_persona"
                }
            ],
        }
    ]
}