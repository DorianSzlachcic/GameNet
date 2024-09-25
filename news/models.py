from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field
from cloudinary.models import CloudinaryField

# Create your models here.

class News(models.Model):
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=256)
    lead = models.TextField(max_length=1024, default="Lead of news")
    image = CloudinaryField("news_image", null=True, blank=True)
    content = CKEditor5Field()
    created_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
