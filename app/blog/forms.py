from . import models

from django import forms


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)

class CommentPostForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ("name", "email", "body")
