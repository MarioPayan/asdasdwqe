MENUWARE_MENU = {
    "LEFT_NAV_MENU": [
        {
            "name": "Auditoría",
            "url": "auditoria:listar",
            "render_for_authenticated": True,
            "render_for_user_when_has_permission": "auditoria.change_auditorialog",
            "icon": "fa fa-ban"
        }
    ]
}