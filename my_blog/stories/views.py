from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404

from .models import Stories, Tag, Category

menu = [
    {'title': "На главную", 'url_name': 'index'},
    {'title': "О сайте", 'url_name': 'about'},
    {'title': "Написать историю", 'url_name': 'add_story'},
]


# Create your views here.
def about(request):
    """A view that displays about-page"""
    return render(request, 'stories/about.html', context={})


def addstory(request):
    """A view that displays a form to add a story"""
    return render(request, 'stories/addstory.html', context={})


def index(request):
    """A view that displays main page with all stories"""
    return render(request, 'stories/index.html', context={'cat_selected':0})


def story(request, story_slug: str):
    """A view that displays a certain story with the possibility to edit it"""
    QS = get_object_or_404(Stories, slug=story_slug)
    return render(request, 'stories/story.html', context={'queryset': QS})


def tag(request, tag_slug):
    """A view that displays all published stories connected to this tag"""
    tag = get_object_or_404(Tag, slug=tag_slug)
    stories = tag.tags.published.select_related('cat')  # all()
    return render(request, 'stories/index.html', context={'stories': stories,
                                                          'title': 'Тег: ' + tag.name})


def category(request, cat_id):
    """A view that displays all published stories connected to this category"""
    cat = get_object_or_404(Category, id=cat_id)
    stories = cat.stories.published.all()
    return render(request, 'stories/index.html', context={'stories': stories,
                                                          'title': 'Категория: ' + cat.name,
                                                          'cat_selected': cat_id})


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
