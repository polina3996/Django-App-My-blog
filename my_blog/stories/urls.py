from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about, name='about'),
    path('addstory/', views.addstory, name='add_story'),
    path('', views.index, name='index'),
    path('story/<slug:story_slug>/', views.story, name='story')
]

#     path('login/', views.login, name='login'),
#     path('category/<slug:cat_slug>/', views.WomenCategory.as_view(), name='category'),
#     path('tag/<slug:tag_slug>/', views.TagPostList.as_view(), name='tag'),
#     path('edit/<slug:slug>/', views.UpdatePage.as_view(), name='edit_page'),