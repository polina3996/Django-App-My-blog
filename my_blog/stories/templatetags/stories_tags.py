from django import template
from django.db.models import Count

from .. import views
from ..models import Tag, Category

# object Library to register our new tags
register = template.Library()


@register.inclusion_tag('stories/tags.html')
def show_tags():
    """An inclusion user's tag to get a list of tags, connected to any stories"""
    tags = Tag.objects.annotate(total=Count("tags")).filter(total__gt=0)
    # parameter 'tags' goes to template 'tags'
    return {'tags': tags}


@register.inclusion_tag('stories/categories.html')
def show_categories(cat_selected=0):
    """An inclusion user's tag to get a list of categories, connected to any stories"""
    categories = Category.objects.annotate(total=Count("stories")).filter(total__gt=0)
    # parameter 'categories' goes to template 'categories'
    return {'categories': categories,
            'cat_selected': cat_selected}
