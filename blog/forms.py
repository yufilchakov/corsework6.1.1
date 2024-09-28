from django import forms
from .models import Blog


class BlogCreateForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('name', 'contents_article', 'image', 'number_views', 'date_published')
        