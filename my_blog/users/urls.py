from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    # path('register/', views.register, name='register'),
    # path('profile/', views.ProfileUser.as_view(), name='profile'),
]