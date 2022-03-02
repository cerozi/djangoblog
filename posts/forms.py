from django.forms import ModelForm
from .models import Post
from .models import Comments

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('texto', )

class CommentForm(ModelForm):
    class Meta:
        model = Comments
        fields = ('texto', )