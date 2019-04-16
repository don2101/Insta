from django import forms
from .models import Post, Comment

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
    content = forms.CharField(widget = forms.TextInput(attrs={
       'placeholder': '댓글을 입력하세요.',
       'class': 'form-control d-inline col-8'
   }), label='')
    
    class Meta:
        model = Comment
        fields = ['content']
