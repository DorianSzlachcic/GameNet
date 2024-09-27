from django.forms import ModelForm

from .models import Review
from django_ckeditor_5.widgets import CKEditor5Widget

class ReviewForm(ModelForm):   
    class Meta:
        model = Review
        fields = ["title","game","lead","points","image","content","summary"]
        widgets = {
              "content": CKEditor5Widget()
          }
