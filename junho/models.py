from ast import Store
from email.mime import image
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

class User(AbstractUser):
    question = models.CharField(max_length=100,blank=False, null=False)
    answer = models.CharField(max_length=100,blank=False, null=False)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username = models.CharField(
        verbose_name='username',
        max_length=10,
        unique=True,
    )

class Objectss(models.Model):
    id = models.AutoField(primary_key=True)
    store = models.CharField(max_length=100,blank=False, null=False)
    name = models.CharField(max_length=100,blank=False, null=False)
    type = models.CharField(max_length=100,blank=False, null=False)
    price = models.IntegerField(blank=False, null=False)
    image = models.ImageField(upload_to='image/',blank=False, null=False)
    
class Board(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20,blank=False, null=False)
    title = models.CharField(max_length=50, null=False, blank=False)
    content = models.TextField(null=False,blank=False)
    create_date= models.DateTimeField(default=timezone.now,blank=False, null=False)
    modified_date = models.DateTimeField(auto_now=True)
    
class BoardComment(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=100,null=False,blank=False)
    username = models.CharField(max_length=20,blank=False, null=False)
    board_id = models.ForeignKey('Board',related_name='boardcomment',on_delete=models.CASCADE,db_column='board_id')
    create_date= models.DateTimeField(default=timezone.now,blank=False, null=False)
    modified_date = models.DateTimeField(auto_now=True)
    
class Posts(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.TextField(blank=False, null=False)
    content = models.TextField(blank=False, null=False)
    nickname = models.CharField(max_length=10,blank=False, null=False)
    likes = models.ManyToManyField(User,related_name='likes_user',blank=True, null=True)
    likes_cnt = models.IntegerField(blank=True, null=True)
    # image = models.ImageField(blank=True, null=True)
    choiceitem = models.ManyToManyField(Objectss,through='Poststag',related_name='Objects_id',blank=False, null=False)
    create_date= models.DateTimeField(default=timezone.now,blank=False, null=False)
    modified_date = models.DateTimeField(auto_now=True)

class Poststag(models.Model):
    objectss = models.ForeignKey(Objectss, on_delete=models.CASCADE)
    posts = models.ForeignKey(Posts, on_delete=models.CASCADE)
    name = models.CharField(max_length=100,blank=True, null=True)
    type = models.CharField(max_length=100,blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    image = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'junho_posts_choiceitem'

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=100)
    nickname = models.CharField(max_length=10,blank=False, null=False)
    post_id = models.ForeignKey('Posts',related_name='post',on_delete=models.CASCADE,db_column='post_id')
    create_date= models.DateTimeField(default=timezone.now,blank=False, null=False)
    modified_date = models.DateTimeField(auto_now=True)

class GS25(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,blank=True, null=True)
    type = models.CharField(max_length=100,blank=True, null=True)
    price = models.CharField(max_length=100,blank=True, null=True)
    image = models.TextField(blank=True, null=True)
    GIFTimage = models.TextField(blank=True, null=True)
    
class MINISTOP(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,blank=True, null=True)
    type = models.CharField(max_length=100,blank=True, null=True)
    price = models.CharField(max_length=100,blank=True, null=True)
    GIFTname = models.CharField(max_length=100,blank=True, null=True)
    image = models.TextField(blank=True, null=True)
    GIFTimage = models.TextField(blank=True, null=True)

class CU(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,blank=True, null=True)
    type = models.CharField(max_length=100,blank=True, null=True)
    price = models.CharField(max_length=100,blank=True, null=True)
    image = models.TextField(blank=True, null=True)
