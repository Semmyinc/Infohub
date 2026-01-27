from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Blog
# Create your views here.

def home(request):
    stories = Blog.objects.filter(is_featured=True, status='published')
    # stories = Blog.objects.all()
    context = {'stories':stories}
    # return HttpResponse("Ok")
    return render(request, 'home.html', context)

def stories(request):
    stories = Blog.objects.all()
    context = {'stories':stories}
    return render(request, 'stories/stories.html', context)

def story(request, slug):
    # blog = get_object_or_404(Blog, slug=slug, status='published')

    context = {}
    return render(request, 'stories/story.html', context)