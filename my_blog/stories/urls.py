from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about, name='about'),
    path('addstory/', views.addstory, name='add_story'),
    path('', views.index, name='index'),
    path('story/<slug:story_slug>/', views.story, name='story'),
    path('tag/<slug:tag_slug>/', views.tag, name='tag'),
    path('category/<int:cat_id>/', views.category, name='category'),
]

#     path('login/', views.login, name='login'),
#
#
#     path('edit/<slug:slug>/', views.UpdatePage.as_view(), name='edit_page'),