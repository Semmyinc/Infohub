"""
URL configuration for infohub project.

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
from django.contrib import admin
from django.urls import path, include
from stories import views as stories_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.home, name='home'),
    path('team/', include('team.urls')),
    # path('about/', views.about, name='about'),
    path('stories/', include('stories.urls')),
    path('categories/', include('category.urls')),
    path('category_posts/<slug:slug>', stories_views.category_posts, name='category_posts'),
    path('categories/add_category/', stories_views.add_category, name='add_category'),
    path('categories/edit_category/<slug:slug>/', stories_views.edit_category, name='edit_category'),
    path('categories/delete_category/<slug:slug>/', stories_views.delete_category, name='delete_category'),
    path('stories/', include('stories.urls')),
    path('add_story/', stories_views.add_story, name='add_story'),
    path('edit_story/<slug:slug>/', stories_views.edit_story, name='edit_story'),
    path('delete_story/<slug:slug>/', stories_views.delete_story, name='delete_story'),
    path('search/', stories_views.search, name='search'),
    path('users/', include('users.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
