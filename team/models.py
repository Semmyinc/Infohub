from django.db import models
from users.models import Users
# Create your models here.
class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.name
    
class AboutUs(models.Model):
    name = models.ForeignKey(Users, on_delete=models.DO_NOTHING)
    facebook = models.CharField(max_length=100)
    linkedin = models.CharField(max_length=100)
    twitter = models.CharField(max_length=100)
    instagram = models.CharField(max_length=100)

