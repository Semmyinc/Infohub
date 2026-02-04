from . import views
from django.urls import path

urlpatterns = [
    path('', views.stories, name='stories'),
    path('<slug:slug>/', views.story, name='story'),
    # path('<slug:slug>/comment_reply/<int:pk>', views.comment_reply, name='comment_reply'),
    path('add_story/', views.add_story, name='add_story'),
]