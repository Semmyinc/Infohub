from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

# create model for user admin - (pages involved - model, admin & settings)
class UsersManager(BaseUserManager):

    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User must provide an email address')
        
        if not username:
            raise ValueError('User must provide a username')
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    # create super user 
    def create_superuser(self, first_name, last_name, username, email, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
            password = password
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        # user.is_superadmin = True #Had this commented during my personal research to make my custom usermodel work effectively
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Users(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=50)
    email = models.EmailField(unique=True)

    # required fields 
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    

    # set login field 

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UsersManager()

    # groups = models.ManyToManyField('auth.Group', related_name='users_set', blank=True)

    # user_permissions = models.ManyToManyField('auth.Remission', related_name='users_set', blank=True)

    def __str__(self):
        return self.email
    
    # def has_perm(self, perm, obj=None):
    #     return self.is_superuser or self.is_admin
    
    # def has_module_perms(self, app_label):
    #     return True
    

    class Meta:
        verbose_name_plural = 'Users'

    def fullname(self):
        return f'{self.first_name} {self.last_name}'
    

sex = (
('male', 'male'),
('female', 'female'),

)
class Profile(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    gender = models.CharField(max_length=20, choices=sex)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    image = models.ImageField(upload_to='uploads/myprofile_photo/', default='uploads/myprofile_photo/default.jpg')

    def __str__(self):
        return self.user.username