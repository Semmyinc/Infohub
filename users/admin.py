from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Users
# Register your models here.


class UsersAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'date_joined', 'last_login', 'is_active', 'is_staff')
    list_display_links = ('email', 'first_name', 'last_name', 'username')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('email',)   #('-date_joined',)
    model = Users
    filter_horizontal = ('groups', 'user_permissions')
    list_filter = ()
    fieldsets = ( 
        (None, {'fields':('email', 'password')}), 
        ('Personal Information', {'fields': ('first_name', 'last_name', 'username')}),
        ('Permissions', {'fields':('is_active', 'is_staff', 'is_admin', 'is_superuser', 'groups', 'user_permissions')}), 
        ('Important Dates', {'fields':('date_joined', 'last_login')}),
    )

    add_fieldsets = (
        (None, {'classes':('wide',), 'fields': ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')}),
        ('Permissions', {'fields':('is_active', 'is_staff', 'is_admin', 'is_superuser', 'groups', 'user_permissions')}), 
    )
    
    # add_fieldsets = UserAdmin.add_fieldsets + (('Custom Fields', {'fields':('groups', 'user_permissions')}),)

admin.site.register(Users, UsersAdmin)

# admin.site.register(Users)
