from django.contrib.auth.forms import UserCreationForm,UserChangeForm,SetPasswordForm
from .models import Posts, User
from django import forms

class SignupForm(UserCreationForm):
      class Meta:
          model = User
          fields = ['username', 'password1', 'password2', 'question','answer','email']
          
# class PasswdFindForm(SetPasswordForm):
#       class Meta:
#           model = User
#           fields = ['new_password1','new_password2']
          
class PostsForm(forms.ModelForm):
      class Meta:
          model = Posts
          fields = ['title', 'content','nickname']