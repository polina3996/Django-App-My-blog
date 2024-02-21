from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about, name='about'),
    path('addstory/', views.AddStoryView.as_view(), name='add_story'),
    path('edit/<slug:slug>/', views.EditStoryView.as_view(), name='edit_story'),
    path('delete/<slug:slug>/', views.DeleteStoryView.as_view(), name='delete_story'),
    path('', views.IndexView.as_view(), name='index'),
    path('story/<slug:story_slug>/', views.StoryView.as_view(), name='story'),
    path('category/<slug:cat_slug>/', views.CategoryView.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.TagView.as_view(), name='tag'),
]
