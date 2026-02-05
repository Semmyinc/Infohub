from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Blog, Category, Comment, CommentReply
from django.contrib import messages
from .forms import CategoryForm, StoryForm
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


# search functionality 
def search(request):
    if request.method == 'POST':
        keyword = request.POST['keyword']
        searched = Blog.objects.filter(Q(name__icontains=keyword)
                                     |Q(category__name__icontains=keyword)
                                     |Q(author__username__icontains=keyword)
                                     |Q(author__email__icontains=keyword)
                                     |Q(author__first_name__icontains=keyword)
                                     |Q(author__last_name__icontains=keyword)
                                    #  |Q(author__fullname__icontains=keyword)
                                     |Q(author__phone__icontains=keyword)
                                     |Q(summary__icontains=keyword)
                                     |Q(body__icontains=keyword)
                                     |Q(status__icontains=keyword)
                                     |Q(is_featured__icontains=keyword)
                                     |Q(created_at__icontains=keyword)
                                     |Q(modified_at__icontains=keyword)
        )
    paginator = Paginator(searched, 2)
    page_number = request.GET.get('page')
    try:
        paged_search = paginator.get_page(page_number)
    except PageNotAnInteger:
        paged_search = paginator.get_page(1)
    except EmptyPage:
        paged_search = paginator.get_page(paginator.num_pages)
                                        
    search_count = searched.count()

    context = {'searched':paged_search, 'search_count':search_count}
    return render(request, 'stories/search.html', context)

# function to create a new blog
@login_required(login_url='login')
def add_story(request):
    form = StoryForm()
    if request.method == 'POST':
        form = StoryForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            story = form.save(commit=False)
            story.author = request.user
            story.save()
            story_name = form.cleaned_data['name']
            story.slug = f'{slugify(story_name)}-{str(story.id)}'
            story.save()
            messages.success(request, f'{story_name} has been added successfully')
            return redirect('stories')
        messages.error(request, f'Errors detected while filling form. Please try again')
        return redirect('add_story')

    context = {'form':form}
    return render(request, 'stories/add_story.html', context)

@login_required(login_url='login')
def edit_story(request, slug):
    story = get_object_or_404(Blog, slug=slug, status='published' )
    if request.method == 'POST':
        form = StoryForm(request.POST, request.FILES, instance=story)
        if form.is_valid():
            story_name = form.cleaned_data['name']
            form.save()
            messages.success(request, f'{story_name} has been updated successfully')
            return redirect('dashboard_stories')
        messages.error(request, f'Errors detected while submitting form. Please try again')
        # return reverse(HttpResponseRedirect('edit_category', args=[''])
        return redirect('home')
    
    form = StoryForm(instance=story)
    context = {'form':form}
    return render(request, 'stories/edit_story.html', context)

@login_required(login_url='login')
def delete_story(request, slug):
    story = get_object_or_404(Blog, slug=slug)
    if request.method == 'POST':
        story.delete()
        messages.success(request, f'story deleted successfully')
        return redirect('dashboard_stories')
    
    context = {'story':story} 
    return render(request, 'stories/delete_story.html', context)

# function to create a new category
@login_required(login_url='login')
def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST or None)
        if form.is_valid():
            category_name = form.cleaned_data['name']
            # slug = form.cleaned_data.get('slug')
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            name = form.cleaned_data['name']
            category.slug = f'{slugify(name)}-{str(category.id)}'
            category.save()
            messages.success(request, f'{category_name} has been added successfully')
            return redirect('home')
        messages.error(request, f'Errors detected while filling form. Please try again')
        return redirect('add_category')
    
    context = {'form':form}
    return render(request, 'stories/add_category.html', context)

@login_required(login_url='login')
def edit_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['name']
            form.save()
            messages.success(request, f'{category_name} has been updated successfully')
            return redirect('dashboard_categories')
        messages.errors(request, f'Errors detected while submitting form. Please try again')
        # return reverse(HttpResponseRedirect('edit_category', args=[''])
        return redirect('add_category')
    
    form = CategoryForm(instance=category)
    context = {'form':form}
    return render(request, 'stories/edit_category.html', context)

@login_required(login_url='login')
def delete_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    if request.method == 'POST':
        category.delete()
        messages.success(request, f'Category name deleted successfully')
        return redirect('dashboard_categories')
    
    context = {'category':category} 
    return render(request, 'stories/delete_category.html', context)


def categories(request):
    context = {}
    return render(request, 'stories/categories.html', context)

def stories(request):
    stories = Blog.objects.all().order_by('-created_at')
    paginator = Paginator(stories, 2)
    page_number = request.GET.get('page')
    try:
        paged_stories = paginator.get_page(page_number)
    except PageNotAnInteger:
        paged_stories = paginator.get_page(1)
    except EmptyPage:
        paged_stories = paginator.get_page(paginator.num_pages)
        
    context = {'stories':paged_stories}
    return render(request, 'stories/stories.html', context)

    

def story(request, slug):
    blog = get_object_or_404(Blog, slug=slug, status='published')
    
    
    if request.method == 'POST':
        comment = Comment()
        comment.blog = blog
        comment.user = request.user
        comment.body = request.POST['message']
        comment.save()

    comments = Comment.objects.filter(blog=blog)        
    comments_count = comments.count() 

    context = {'blog':blog, 'comments':comments, 'comments_count':comments_count}
    return render(request, 'stories/story.html', context)

# def comment_reply(request, slug, pk):
#     blog = get_object_or_404(Blog, slug=slug, status='published')
#     # comments = Comment.objects.filter(blog=blog)
    
#     if request.method =='POST':
#         comment_reply = CommentReply()
#         comment_reply.user = request.user
#         comment_reply.body = request.POST['reply']
#         comment_reply.save()

#     comment = Comment.objects.get(blog=blog, id=pk)
#     comment_reply = CommentReply.filter(comment=comment)
#     context = {'comment_reply':comment_reply, 'comment':comment}
#     return render(request, 'stories/comment_reply.html', context)

def category_posts(request, slug):
    try:
        # category = Category.objects.get(slug=slug)
        # category_posts = Blog.objects.filter(category=category, status='published')
        category_posts = Blog.objects.filter(category__slug=slug, status='published') #the above 2 lines of code replaced by this single line
    except Blog.DoesNotExist:
        messages.warning(request, f'Post(s) in this category is/are not available yet')
        return redirect('home')
    
    paginator = Paginator(category_posts, 2)
    page_number = request.GET.get('page')
    try:
        paged_category_posts = paginator.get_page(page_number)
    except PageNotAnInteger:
        paged_category_posts = paginator.get_page(1)
    except EmptyPage:
        paged_category_posts = paginator.get_page(paginator.num_pages)
    
    context = {'category_posts':paged_category_posts}
    return render(request, 'category_posts.html', context)