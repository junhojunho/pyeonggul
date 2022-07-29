from secrets import choice
from .models import *
from rest_framework import serializers
from urllib.parse import unquote, quote, quote_plus, urlencode
from django.db.models import F, Sum, Count, Case, When

class ObjectsSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    class Meta:
        model = Objectss
        fields = '__all__'
        


        
class PoststagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poststag
        fields ='__all__'
        
class BoardCommentSerializer(serializers.ModelSerializer):
    reply = serializers.SerializerMethodField()
    
    class Meta:
        model = BoardComment
        fields =('id','comment','username','board_id','parent','create_date','modified_date','reply')
        
    def get_reply(self, instance):
        serializer = self.__class__(instance.reply, many=True)
        serializer.bind('', self)
        return serializer.data

class BoardSerializer(serializers.ModelSerializer):
    boardcomment = BoardCommentSerializer(many=True,read_only=True)
    class Meta:
        model = Board
        fields =('id','title','content','username','create_date','modified_date','boardcomment','hits','image')

class CommentSerializer(serializers.ModelSerializer):
    reply = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields =('id','comment','nickname','post_id','parent','create_date','modified_date','reply')
        
    def get_reply(self, instance):
        serializer = self.__class__(instance.reply, many=True)
        serializer.bind('', self)
        return serializer.data

class PostsSerializer(serializers.ModelSerializer):           
    post = CommentSerializer(many=True,read_only=True)
    a = PoststagSerializer(source = 'poststag_set',many=True)
    class Meta: 
        model = Posts
        fields = ('id','title','content','nickname','likes_cnt','create_date','modified_date','likes','post','a','image') 
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    
class ObjectsSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    class Meta:
        model = Objectss
        fields = '__all__'

class MinistopSerializer(serializers.ModelSerializer):
    class Meta:
        model = MINISTOP
        fields = '__all__'
class Gs25Serializer(serializers.ModelSerializer):
    class Meta:
        model = GS25
        fields = '__all__'
class CuSerializer(serializers.ModelSerializer):
    class Meta:
        model = CU
        fields = '__all__'

