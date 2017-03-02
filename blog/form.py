from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    # <input type="text">
    name = forms.CharField(max_length=25)
    # EmailField:
    # if not email-address in email: raise forms.ValidationError
    email = forms.EmailField()
    to = forms.EmailField()
    # use 'widget' <input type="textarea">
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    # 会自动根据 Model 里的 model.CharField 自动生成form.CharField
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')