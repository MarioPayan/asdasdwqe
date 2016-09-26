from django import template
from django.conf import settings

from ..menu import generate_menu
from ..utils import get_func
from .. import defaults as defs


MENUS_NAME = ".menus.MENUWARE_MENU"


register = template.Library()


@register.assignment_tag(takes_context=True)
def get_menu(context, name):
    """
    Returns a consumable menu list for a given menu name, if the name is found in the
    `MENUWARE_MENU` field of settings.py, or it returns an empty list.
    """

    menu_list = get_menus_from_apps(name)
    return generate_menu(context['request'], menu_list)


def get_menus_from_apps(name):
    installed_apps = getattr(settings, "INSTALLED_APPS", defs.MENU_NOT_FOUND)
    if installed_apps == defs.MENU_NOT_FOUND:
        return installed_apps

    menu_list = []
    for app in installed_apps:
        menu_dict = get_func(app + MENUS_NAME)
        if not menu_dict:
            continue
        menu_list += menu_dict.get(name, [])
    return menu_list
