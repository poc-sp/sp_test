from django import forms

from .models import ArticleComment


class CommentForm(forms.ModelForm):
    class Meta:
        model = ArticleComment
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5, 'cols': 30}),
        }
        fields = ('content',)
