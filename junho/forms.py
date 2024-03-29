from distutils.errors import CompileError
from xml.etree.ElementTree import Comment
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,SetPasswordForm
from .models import *
from django import forms

class SignupForm(UserCreationForm):
      class Meta:
          model = User
          fields = ['username', 'password1', 'password2', 'question','answer','email']
          
class BoardForm(forms.ModelForm):
      class Meta:
          model = Board
          fields = ['username','title','content','image']
          
class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['username','title','content','image']
          
class PostsForm(forms.ModelForm):
      class Meta:
          model = Posts
          fields = ['title', 'content','nickname','image']

class BoardCommentForm(forms.ModelForm):
      class Meta:
          model = BoardComment
          fields = ['username','comment']
          
class CommentForm(forms.ModelForm):
      class Meta:
          model = Comment
          fields = ['comment']
        
        