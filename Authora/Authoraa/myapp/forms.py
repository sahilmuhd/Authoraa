from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'is_published']
        widgets = {
            'content': forms.Textarea(attrs={'id': 'editor'}),
        }
