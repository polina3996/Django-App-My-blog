from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


# Create your models here.
class PublishedManager(models.Manager):
    """Manager that takes from the database only PUBLISHED stories"""
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Stories.Status.PUBLISHED)


class Stories(models.Model):
    class Status(models.IntegerChoices):
        """Class with options for the story (published or not)"""
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, null=False, verbose_name="Slug", validators=[
        MinLengthValidator(5, message="Минимум 5 символов"),
        MaxLengthValidator(100, message="Максимум 100 символов"),
    ])
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", default=None,
                              blank=True, null=True, verbose_name="Фото")
    content = models.TextField(blank=True, verbose_name="Текст рассказа")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                       default=Status.DRAFT, verbose_name="Статус")

    # object of model Category.
    # attribute + field in Stories: 'cat_id'
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='stories', verbose_name="Категории")

    # object of model Tag.
    # NO field in Stories: new mid-table + attribute
    tags = models.ManyToManyField('Tag', blank=True, related_name='tags', verbose_name="Теги")

    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='stories', null=True,
                               default=None)

    # to still exist (stories = Stories.objects.all())
    objects = models.Manager()
    # creating a manager, that takes only published stories
    # instead of 'objects' attribute (stories = Stories.published.all())
    published = PublishedManager()

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title)
    #     super(Stories, self).save(*args, **kwargs)

    # how the object of the Stories will be displayed
    def __str__(self):
        return self.title

    class Meta:
        """Metadata of the model Stories(in admin-panel)"""
        verbose_name = "Рассказ"
        verbose_name_plural = "Рассказы"
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]

    def get_absolute_url(self):
        """Object of the Stories can return URL"""
        return reverse('story', kwargs={'story_slug': self.slug})


class Category(models.Model):
    """Model with ManyToOne with Stories"""
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, null=False)

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.name)
    #     super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    # how the object of the Category will be displayed
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Object of the Category can return URL"""
        return reverse('category', kwargs={'cat_slug': self.slug})


class Tag(models.Model):
    """Model with ManyToMany to Stories"""
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, null=False)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.name)
    #     super(Tag, self).save(*args, **kwargs)

    # how the object of the Tag will be displayed
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Object of the Tag can return URL"""
        return reverse('tag', kwargs={'tag_slug': self.slug})
