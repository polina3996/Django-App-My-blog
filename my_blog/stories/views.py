from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy

from .forms import AddStory
from .models import Stories, Tag, Category
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .utils import DataMixin


# Create your views here.
def about(request):
    """A view that displays about-page"""
    return render(request, 'stories/about.html', context={'title': 'О сайте'})


class IndexView(DataMixin, ListView):
    """A Class Based View that displays main page with all stories"""
    template_name = 'stories/index.html'
    context_object_name = 'stories'
    title_page = 'Все истории'
    cat_selected = 0

    def get_queryset(self):
        return Stories.published.all().select_related('cat')


class AddStoryView(DataMixin, LoginRequiredMixin, CreateView):
    """A Class Based View that displays a form to add a story"""
    form_class = AddStory
    template_name = 'stories/addstory.html'
    title_page = 'Добавление истории'
    # if we want to redirect not where 'get_absolute_url' of Stories(connected to this form) leads
    success_url = reverse_lazy('index')


# class AddPage(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, CreateView):
#     permission_required = 'women.add_women' # <приложение>.<действие>_<таблица>
#     def form_valid(self, form):
#         w = form.save(commit=False)
#         w.author = self.request.user
#         return super().form_valid(form)


class EditStoryView(DataMixin, LoginRequiredMixin, UpdateView):
    """A Class Based View that displays some fields of the story to edit it"""
    model = Stories
    # fields from the form AddStory that we want to be edited
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'stories/addstory.html'
    success_url = reverse_lazy('index')
    title_page = 'Редактирование истории'
    # permission_required = 'women.change_women'


# class Edit_Story(PermissionRequiredMixin, DataMixin, UpdateView):



class DeleteStoryView(DataMixin, LoginRequiredMixin, DeleteView):
    """A Class Based View that displays a new template where you can delete the story"""
    model = Stories
    success_url = reverse_lazy('index')
    template_name = "stories/stories_confirm_delete.html"
    # permission_required = 'women.change_women'


# class Delete_Story(PermissionRequiredMixin, DataMixin, UpdateView):


class StoryView(DataMixin, LoginRequiredMixin, DetailView):
    """A Class Based View that displays a certain story"""
    template_name = 'stories/story.html'
    slug_url_kwarg = 'story_slug'
    context_object_name = 'story'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['story'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Stories.published, slug=self.kwargs[self.slug_url_kwarg])


class TagView(DataMixin, ListView):
    """A view that displays all published stories connected to this tag"""
    template_name = 'stories/index.html'
    context_object_name = 'stories'
    # if there are no objects -> 404NotFound
    allow_empty = False

    def get_queryset(self):
        # stories with corresponding category
        return Stories.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        # content of the template
        context = super().get_context_data(**kwargs)
        tag = Tag.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context,
                                      title='Тег: ' + tag.name)


class CategoryView(DataMixin, ListView):
    """A view that displays all published stories connected to this category"""
    template_name = 'stories/index.html'
    context_object_name = 'stories'
    # if there are no objects -> 404NotFound
    allow_empty = False

    def get_queryset(self):
        # stories with corresponding category
        return Stories.published.filter(cat__slug=self.kwargs['cat_slug']).select_related("cat")

    def get_context_data(self, **kwargs):
        # content of the template
        context = super().get_context_data(**kwargs)
        cat = context['stories'][0].cat
        return self.get_mixin_context(context,
                                      title='Категория: ' + cat.name,
                                      cat_selected=cat.pk,
                                      )


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
