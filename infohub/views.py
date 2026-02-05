from django.shortcuts import render
from django.http import HttpResponse
from stories.models import Blog, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
    stories = Blog.objects.all().order_by('-created_at')[:7]
    # comments_count = Comment.objects.filter(blog__slug=slug).count()
    featured_stories = Blog.objects.filter(is_featured=True)
    # featured_comments_count = Comment.objects.filter(blog__slug=slug, blog__is_featured=True).count()

    paginator = Paginator(stories, 2)
    page_number = request.GET.get('page')
    try:
        paged_stories = paginator.get_page(page_number)
    except PageNotAnInteger:
        paged_stories = paginator.get_page(1)
    except EmptyPage:
        paged_stories = paginator.get_page(paginator.num_pages)
                                         
    
    context = {'stories':paged_stories, 'featured_stories':featured_stories}
    # return HttpResponse("Ok")
    return render(request, 'home.html', context)