from django.contrib import admin
from .models import Category, Blog
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Category, CategoryAdmin)
# admin.site.register(Category)
admin.site.register(Blog, BlogAdmin)