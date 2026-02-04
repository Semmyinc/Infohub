from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.category, name='categories')
    # path('category/<slug:slug>/', views.category_posts, name='category_posts'),
]
