from django.forms import ModelForm
from .models import Post, Comment


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['content']

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget.attrs['placeholder'] = 'What\'s on your mind ?'
        self.fields['content'].required = True
        self.fields['content'].label = ''
        self.fields['content'].widget.attrs.update({'class': 'form-control mt-3 mb-1'})


