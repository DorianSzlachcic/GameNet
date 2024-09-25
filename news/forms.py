from django.forms import ModelForm
from django_ckeditor_5.widgets import CKEditor5Widget

from .models import News

class NewsForm(ModelForm):   
    class Meta:
        model = News
        fields = ["title","lead","image","content"]
        widgets = {
              "content": CKEditor5Widget()
          }
