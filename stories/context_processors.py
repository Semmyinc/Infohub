from .models import Category, Blog

def cat_func(request):
    categories = Category.objects.all()
    return dict(categories=categories)

def post_func(request):
    posts = Blog.objects.filter(status='published') #.filter(status='published')
    return dict(posts=posts)