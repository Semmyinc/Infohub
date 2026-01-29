from django.db import models
from users.models import Users
# Create your models here.

class Category(models.Model):
    user = models.ForeignKey(Users,on_delete=models.CASCADE, unique=True, blank=True, null=True)
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


STATUS = (
    ('draft', 'draft'),
    ('published', 'published')
)

class Blog(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(Users, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/blog_image',)
    summary = models.CharField(max_length=255)
    body = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS, default='draft')
    image_pg = models.ImageField(upload_to='uploads/blog_image_on_blog', blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name