from django import forms
from .models import Comment, Reply

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    body = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = Comment
        fields = ('body',)

class ReplyForm(forms.ModelForm):
    body = forms.CharField(label='', widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = Reply
        fields = ('body',)
