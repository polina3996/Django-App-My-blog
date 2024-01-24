from django.contrib import admin, messages
from django.db.models import QuerySet
from django.utils.safestring import mark_safe

from .models import Stories, Category


# Register your models here.
@admin.register(Stories)
class StoriesAdmin(admin.ModelAdmin):
    """Model Stories in admin panel"""
    list_display = ('title', 'author', 'post_photo', 'time_create', 'is_published', 'cat')
    list_filter = ['cat__name', 'is_published']  # 'tag__name'
    list_per_page = 5
    search_fields = ['title__startswith', 'cat__name']
    list_editable = ('is_published', 'cat')
    ordering = ['-time_create', 'title']
    actions = ['set_published', 'set_draft']
    list_display_links = ('title',)
    save_on_top = True
    prepopulated_fields = {"slug": ("title",)}

    fields = ['title', 'author', 'slug', 'content', 'photo', 'post_photo', 'cat', 'tags']
    readonly_fields = ['post_photo']
    filter_horizontal = ['tags',]

    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, QS: QuerySet):
        """Action 1"""
        # QS - is what we've chosen in admin panel
        # count - amount of changed objects
        count = QS.update(is_published=Stories.Status.PUBLISHED)
        # message to superuser
        self.message_user(request, f"Изменено {count} записей.")

    @admin.action(description="Снять с публикации выбранные записи")
    def set_draft(self, request, QS: QuerySet):
        """Action 2"""
        count = QS.update(is_published=Stories.Status.DRAFT)
        self.message_user(request, f"{count} записей сняты с публикации!", messages.WARNING)

    @admin.display(description="Изображение", ordering='content')
    def post_photo(self, s: Stories):
        """Display 1: displays new field in admin panel without adding it to database"""
        if s.photo:
            return mark_safe(f"<img src='{s.photo.url}' width=50>")
        return "Без фото"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Model Category in admin panel"""
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


