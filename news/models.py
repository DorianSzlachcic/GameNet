from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

# Create your models here.

class News(models.Model):
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=256)
    lead = models.TextField(max_length=1024, default="Lead of news")
    image = models.ImageField(null=True, blank=True, upload_to='uploads/news/')
    content = RichTextField()
    created_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)