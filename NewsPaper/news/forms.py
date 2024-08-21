from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class NewsForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'author', 'choice']

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get("content")
        name = cleaned_data.get("title")


        if name == content:
            raise ValidationError(
                "Content can not be the same as the title!"
            )

        return cleaned_data