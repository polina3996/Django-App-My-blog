"""
URL configuration for my_blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.defaults import page_not_found

from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('stories.urls')),
    path("__debug__/", include("debug_toolbar.urls")),

#     path('users/', include('users.urls', namespace="users")),
]

# when DEBUG is False(production): tells Django to take OUR view 'page_not_found' for non-existent pages
handler404 = page_not_found

# when DEBUG is True, we have one more URL (to downloaded files) for test server to take these
# files on MEDIA_URL and view on HTML page
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)