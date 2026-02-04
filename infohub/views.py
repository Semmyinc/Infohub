from django.shortcuts import render
from django.http import HttpResponse
from stories.models import Blog, Comment

def home(request):
    stories = Blog.objects.filter(status='published').order_by('-created_at')
    # comments_count = Comment.objects.filter(blog__slug=slug).count()
    featured_stories = Blog.objects.filter(is_featured=True)
    # featured_comments_count = Comment.objects.filter(blog__slug=slug, blog__is_featured=True).count()

    
    context = {'stories':stories, 'featured_stories':featured_stories}
    # return HttpResponse("Ok")
    return render(request, 'home.html', context)