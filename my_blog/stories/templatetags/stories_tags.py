from django import template
from .. import views

# object Library to register our new tags
register = template.Library()


@register.simple_tag(name='menu')
def get_menu():
    """A simple user's tag to get menu of the app"""
    return views.menu
