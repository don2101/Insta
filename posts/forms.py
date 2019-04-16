from django import forms
from .models import Post

# PostModelForm definition for contrall Post
class PostForm(forms.ModelForm):
    # 1. which input field
    content = forms.CharField(label="content", widget=forms.Textarea(attrs={
        'placeholder': "오늘은 무엇을 하셨나요?"
    }))
    
    # 2. add attitude of input field

    class Meta:
        model = Post
        fields = ['content', 'image']
        
        
class CommentForm(forms.ModelForm):
    content = forms.CharField(label="comment", widget=forms.Textarea())
    
    class Meta:
        model = CommentForm
        fields = ['comment', 'post', 'user']
