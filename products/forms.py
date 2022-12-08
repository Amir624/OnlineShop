from django import forms
from .models import Comment
from ckeditor.widgets import CKEditorWidget


class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Comment
        fields = ('text', )
