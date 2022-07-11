from django.contrib.auth.forms import UserCreationForm,UserChangeForm,SetPasswordForm
from .models import Board, BoardComment, Posts, User
from django import forms

class SignupForm(UserCreationForm):
      class Meta:
          model = User
          fields = ['username', 'password1', 'password2', 'question','answer','email']
          
class BoardForm(forms.ModelForm):
      class Meta:
          model = Board
          fields = ['username','title','content']
          
class PostsForm(forms.ModelForm):
      class Meta:
          model = Posts
          fields = ['title', 'content','nickname']

class BoardCommentForm(forms.ModelForm):
      class Meta:
          model = BoardComment
          fields = ['username','comment']