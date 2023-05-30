from django import forms

from .models import Post


class NewPostForm(forms.ModelForm):
    picture = forms.ImageField(required=True)
    caption = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Caption'}), required=True)
    tags = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Tags | Separate with comma'}), required=True)

    class Meta:
        model = Post
        fields = ['picture', 'caption', 'tags']