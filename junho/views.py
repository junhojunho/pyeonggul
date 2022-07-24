import email
from email.quoprimime import unquote
import encodings
from genericpath import exists
import json
from turtle import title
import jwt
from encodings import utf_8
from itertools import count
from re import L, M
from typing import Counter
from unicodedata import name
from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework import generics
from .models import *
from .serializer import *
from django.db.models import F, Sum, Count, Case, When
from urllib.parse import unquote, quote, quote_plus, urlencode
from rest_framework.renderers import JSONRenderer
from django.http import JsonResponse,HttpResponse
from .forms import  BoardCommentForm, BoardForm, SignupForm , PostsForm
from django.contrib.auth.forms import SetPasswordForm
from rest_framework.permissions import AllowAny
import string
import random
from rest_framework import mixins
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import PBKDF2SHA1PasswordHasher,PBKDF2PasswordHasher
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from junho.utils import *
from .token import account_activation_token,account_activation_token2
from .text import message, passwordmessage
from django.utils.http  import urlsafe_base64_encode,urlsafe_base64_decode
from django.core.mail                import EmailMessage
from django.utils.encoding           import force_bytes, force_str
from django.shortcuts                import redirect
from django.core.validators          import validate_email
from django.core.exceptions          import ValidationError
from django.contrib.sites.shortcuts  import get_current_site
from django.conf import settings
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken

class PostPageNumberPagination(PageNumberPagination):
    page_size = 12
    
class PrivatePageNumberPagination(PageNumberPagination):
    page_size = 10
    

class BestAPIView(APIView):
    def get(self, request,):
        
        paginator = PostPageNumberPagination()
        queryset = Posts.objects.all().order_by('-likes_cnt')
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = PostsSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    def post(self,request):
        postid = request.data.get('postid')
        userid = request.data.get('userid')
        
        if postid or userid == '' or  postid or userid == None:
            Response(status=status.HTTP_400_BAD_REQUEST)
            
        post = get_object_or_404(Posts, id = postid)
        if post.likes.filter(id = userid).exists():
            post.likes.remove(userid)
            post.save()
            b = Posts.objects.all()
            for i in b:
                b = Posts.objects.filter(id=i.id)
                count = b.aggregate(count= Count('likes'))
                Posts.objects.filter(id=i.id).update(likes_cnt = count['count']) 
            
            return Response('좋아요 취소')
        else:
            post.likes.add(userid)
            post.save()
            b = Posts.objects.all()
            for i in b:
                b = Posts.objects.filter(id=i.id)
                count = b.aggregate(count= Count('likes'))
                Posts.objects.filter(id=i.id).update(likes_cnt = count['count']) 
            
            return Response('좋아요')
        
class MainPostsViewSet(ModelViewSet):
                
    queryset = Posts.objects.all().order_by('-create_date')
    serializer_class = PostsSerializer      
    pagination_class = PostPageNumberPagination
    filter_backends = [SearchFilter]
    search_fields = ['title']  

class PostsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        title = request.data.get('title')
        content = request.data.get('content')
        nickname = request.data.get('nickname')
        objectsid = request.data.get('item')
        
        if title == "" or None :
            return Response(1,status=status.HTTP_400_BAD_REQUEST)
        
        if objectsid == []:
            return Response(2,status=status.HTTP_400_BAD_REQUEST)
        
        if content == "" or None:
            return Response(3,status=status.HTTP_400_BAD_REQUEST)        
        
        form = PostsForm(request.data)
        if form.is_valid():
            if objectsid == []:
                return Response({'item':'조합아이템을 선택해주세요'},status=status.HTTP_400_BAD_REQUEST)
            a = Posts.objects.create(
                title = title,
                content = content,
                nickname=nickname,
                likes_cnt=0,
            )
            a.save()
            for b in objectsid:             
                bb = Objectss.objects.get(id=b)
                a.choiceitem.add(b)
                aa = Poststag.objects.filter(posts=a.id).filter(objectss=b)
                aa.update(name = bb.name, type = bb.type, price = bb.price, image = bb.image)
            return Response('작성완료되었습니다')
        else:
            return Response(form.errors,status=status.HTTP_400_BAD_REQUEST)
        
   
class UserAPIView(APIView):
    def post(self, request):
        form = SignupForm(request.data)
        
        if form.is_valid():
            form.save()
            user = User.objects.get(email = request.data.get('email'))
            user.is_active = False
            user.save()
            try: 
                uidb64       = urlsafe_base64_encode(force_bytes(user.id))
                token        = account_activation_token.make_token(user)
                message_data = message(uidb64, token)
                
                mail_title = "이메일 인증을 완료해주세요"
                mail_to    = request.data.get('email')
                email      = EmailMessage(mail_title, message_data, to=[mail_to])
                email.send() 
                return Response('회원가입완료, 이메일 인증을 완료해주세요')

            except KeyError:
                return JsonResponse({"message" : "INVALID_KEY"}, status=400)
            except TypeError:
                return JsonResponse({"message" : "INVALID_TYPE"}, status=400)
            except ValidationError:
                return JsonResponse({"message" : "VALIDATION_ERROR"}, status=400)   
                                            
        return Response(form.errors,status=status.HTTP_400_BAD_REQUEST)
    
class ReEmailTest(APIView):
    def post(self, request):
        
        if User.objects.filter(email = request.data.get('email')).exists():
            user = User.objects.get(email = request.data.get('email'))
            if user.is_active == True:
                return Response({'email':'이미 인증된 이메일 입니다.'})
        else:
            return Response({'email':'가입된 이메일이 아닙니다.'})
        try: 
            uidb64       = urlsafe_base64_encode(force_bytes(user.id))
            token        = account_activation_token.make_token(user)
            message_data = message(uidb64, token)
                
            mail_title = "이메일 인증을 완료해주세요"
            mail_to    = request.data.get('email')
            email      = EmailMessage(mail_title, message_data, to=[mail_to])
            email.send() 
            return Response({'email':'이메일을 확인하여 이메일 인증을 완료해주세요'})

        except KeyError:
            return JsonResponse({"message" : "INVALID_KEY"}, status=400)
        except TypeError:
            return JsonResponse({"message" : "INVALID_TYPE"}, status=400)
        except ValidationError:
            return JsonResponse({"message" : "VALIDATION_ERROR"}, status=400)   

    
    

class Activate(APIView):
    def get(self, request, uidb64, token):
        try:
            uid  = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            
            if account_activation_token.check_token(user, token):
                user.is_active = True
                user.save()

                return redirect('http://54.180.193.83:8080/#/login')
            else:
                return redirect('http://54.180.193.83:8080/#/notpage')
                
            
        except:
            return redirect('http://54.180.193.83:8080/#/notpage')
       
        
class UserPasswdFind(APIView):
    def post(self, request):  
        question = request.data.get('question')
        answer = request.data.get('answer')
        try:
            user = User.objects.get(email = request.data.get('email'))
        except:
            return Response({'email':'가입된 이메일이 아닙니다.'},status=status.HTTP_400_BAD_REQUEST)
        
        if user.question == question and user.answer == answer: 
            try: 
                uidb64       = urlsafe_base64_encode(force_bytes(user.id))
                token        = account_activation_token2.make_token(user)
                message_data = passwordmessage(uidb64, token)
                
                mail_title = "비밀번호 변경 후 로그인 해주세요"
                mail_to    = request.data.get('email')
                email      = EmailMessage(mail_title, message_data, to=[mail_to])
                email.send() 
                
                return Response('가입하신 이메일을 확인해주세요.')
            except KeyError:
                return JsonResponse({"message" : "INVALID_KEY"}, status=400)
            except TypeError:
                return JsonResponse({"message" : "INVALID_TYPE"}, status=400)
            except ValidationError:
                return JsonResponse({"message" : "VALIDATION_ERROR"}, status=400)
        else:
            return Response({'question':'질문과 답이 일치하지 않습니다.'},status=status.HTTP_400_BAD_REQUEST)
        
        
        
class PasswdFind(APIView):
    def get(self, request, uidb64, token):
        try:
            uid  = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            
            if account_activation_token2.check_token(user, token):
                return redirect('http://54.180.193.83:8080/#/login/loginFind/pwChange/'+uidb64+'/'+token)
            else:
                return redirect('http://54.180.193.83:8080/#/notpage')
        except: 
            return redirect('http://54.180.193.83:8080/#/notpage')
        
    def post(self, request):
        try:
            uid  = force_str(urlsafe_base64_decode(request.data.get('uidb64')))
            token = request.data.get('token')
            user = User.objects.get(pk=uid)
            if account_activation_token2.check_token(user, token):
                data = {
                    'new_password1': request.data.get('new_password1'),
                    'new_password2': request.data.get('new_password2')
                }
                form = SetPasswordForm(user, data)
                if form.is_valid():
                    form.save()
                    # user.password = make_password(password)
                else:
                    return Response(form.errors,status=400)
                return Response(status=200)
            return JsonResponse({'message':'error'}, status=400)
        except KeyError:
            return JsonResponse({"message" : "INVALID_KEY"}, status=400)
        except TypeError:
            return JsonResponse({"message" : "INVALID_TYPE"}, status=400)
        except ValidationError:
            return JsonResponse({"message" : "VALIDATION_ERROR"}, status=400)
        except AssertionError:
            return JsonResponse({"message" : "VALIDATION_ERROR"}, status=400)
 
        
class UserIdFind(APIView):
    def post(self,request):
        username = request.data.get('username')
        question = request.data.get('question')
        answer = request.data.get('answer')
        
        a = get_object_or_404(User,username=username)
        
        if a.question == question and a.answer == answer:
            useremail,b = a.email.split('@')
            useremail = useremail.replace(useremail[len(useremail)-4:len(useremail)],'****')
            return Response(useremail+'@'+ b) 
        else:
            return Response({'question':'질문과 답이 일치하지 않아요'},status=status.HTTP_400_BAD_REQUEST)


class OverLapEmail(APIView):
    def get(self,request):
        if User.objects.filter(email = self.request.query_params.get('email')).exists():
            return Response({'email':'사용자의 Email address은/는 이미 존재합니다'})
        else:
            return Response({'email':'사용 가능한 이메일 입니다.'})
 
class OverLapNickname(APIView):
    def get(self,request):
        if User.objects.filter(username = self.request.query_params.get('nickname')).exists():
            return Response({'nickname':'사용자의 Username은/는 이미 존재합니다.'})
        else:
            return Response({'nickname':'사용 가능한 닉네임 입니다.'})
            
class ObjectsPostsSearch(APIView):
    def get(self,request):
        objectss_id = self.request.query_params.get('objects_id')
        paginator = PostPageNumberPagination()
        queryset = Posts.objects.filter(choiceitem = objectss_id)
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = PostsSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
class ObjectsAPIView(generics.ListAPIView):
    
    serializer_class = ObjectsSerializer
    queryset = Objectss.objects.all()
        
    def get(self,request):
        serializer = ObjectsSerializer(Objectss.objects.filter(store=self.request.query_params.get('data')),many=True)
        return Response(serializer.data)
    
    def post(self,request):
        Objectss.objects.create(
            store = request.data.get('store'),
            name = request.data.get('name'),
            type = request.data.get('type'),
            price = request.data.get('price'),
            image = request.data.get('image')
        )
        serializer = ObjectsSerializer(Objectss.objects.all(),many=True)
        return Response(serializer.data)
    
class PostsDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer
    
    def update(self,request,pk):
        title = request.data.get('title')
        content = request.data.get('content')
        nickname = request.data.get('nickname')
        objectsid = request.data.get('item')
        a = Posts.objects.get(id=pk)
        form = PostsForm(request.data)
        if form.is_valid():
            if a.nickname == nickname:
                a.title = title
                a.content = content
                a.save()
                aa = Poststag.objects.filter(posts=a.id)
                aa.delete() 
                for b in objectsid:             
                    bb = Objectss.objects.get(id=b)
                    a.choiceitem.add(b)
                    aa = Poststag.objects.filter(posts=a.id).filter(objectss=b)
                    aa.update(name = bb.name, type = bb.type, price = bb.price, image = bb.image)
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(form.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request,pk):
        a = Posts.objects.get(id=pk)
        if a.nickname == request.data.get('nickname'):
            self.perform_destroy(a)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    
    def update(self,request,pk):
        a = Comment.objects.get(id=pk)
        if a.nickname == self.request.data.get('nickname'):
            a.comment = self.request.data.get('comment')
            a.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request,pk):
        a = Comment.objects.get(id=pk)
        if a.nickname == request.data.get('nickname'):
            self.perform_destroy(a)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

class BoardAPIView(generics.ListAPIView):
    
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = BoardSerializer
    queryset = Board.objects.all().order_by('-create_date')
    
    filter_backends = [SearchFilter]
    search_fields = ['title','content']
    
    # @action(detail=False, methods=['get'])
    # def search(self,request):
    #     paginator = PageNumberPagination()
    #     paginator.page_size = 20
    #     queryset = Board.objects.filter(title=self.request.query_params.get('title'))
    #     result_page = paginator.paginate_queryset(queryset, request)
    #     serializer = BoardSerializer(result_page, many=True)
    #     return paginator.get_paginated_response(serializer.data)
    
    def post(self,request):
        form = BoardForm(request.data)
        if form.is_valid():
            form.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(form.errors,status=status.HTTP_400_BAD_REQUEST)
        
class BoardDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    
    def get(self,reqeust,pk):
        hitcount = get_object_or_404(Board, id = pk)
        hitcount.hits += 1
        hitcount.save()
        serializers = BoardSerializer(hitcount)
        return Response(serializers.data)

        
    def update(self,request,pk):
        a = Board.objects.get(id=pk)
        form = BoardForm(request.data)
        if a.username == self.request.data.get('username'):
            if form.is_valid():
                a.content = self.request.data.get('content')
                a.title = self.request.data.get('title')
                a.save()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(form.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request,pk):
        a = Board.objects.get(id=pk)
        if a.username == request.data.get('username'):
            self.perform_destroy(a)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class BoardCommentAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = BoardComment.objects.all()
    serializer_class = BoardCommentSerializer
    

class BoardCommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = BoardComment.objects.all()
    serializer_class = BoardCommentSerializer
    
        
    def update(self,request,pk):
        a = BoardComment.objects.get(id=pk)
        form = BoardCommentForm(request.data)
        if a.username == self.request.data.get('username'):
            if form.is_valid():
                a.comment = self.request.data.get('comment')
                a.save()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(form.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request,pk):
        a = BoardComment.objects.get(id=pk)
        if a.username == request.data.get('username'):
            self.perform_destroy(a)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class PrivatePosts(APIView):
    def get(self,request):
        username = self.request.query_params.get('username')
        paginator = PrivatePageNumberPagination()
        queryset = Posts.objects.filter(nickname = username).order_by('-create_date')
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = PostsSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
class PrivateLikes(APIView):
    def get(self,request):
        user_id = self.request.query_params.get('user_id')
        paginator = PrivatePageNumberPagination()
        queryset = Posts.objects.filter(likes = user_id).order_by('-create_date')
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = PostsSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
class PrivateBoard(APIView):
    def get(self,request):
        username = self.request.query_params.get('username')
        paginator = PrivatePageNumberPagination()
        queryset = Board.objects.filter(username = username).order_by('-create_date')
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = BoardSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

class PrivateBoardComment(APIView):
    def get(self,request):
        username = self.request.query_params.get('username')
        paginator = PrivatePageNumberPagination()
        queryset = BoardComment.objects.filter(username = username).order_by('-create_date')
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = BoardCommentSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
class PrivatePostsComment(APIView):
    def get(self,request):
        nickname = self.request.query_params.get('username')
        paginator = PrivatePageNumberPagination()
        queryset = Comment.objects.filter(nickname = nickname).order_by('-create_date')
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = CommentSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
class PersonalInformation(APIView):
    def update(self,request):
        
        user = get_object_or_404(username=request.data.get('usernama'))
        if request.data.get('new_password1')=='':
            user.question = request.data.get('question')
            user.answer = request.data.get('answer')
            user.save()
            return Response(status=200)
        
        else:   
            data = {
            'new_password1': request.data.get('new_password1'),
            'new_password2': request.data.get('new_password2')
            }
            form = SetPasswordForm(user, data)
            if form.is_valid():
                user.question = request.data.get('question')
                user.answer = request.data.get('answer')
                form.save()
                user.save()
                return Response(status=200)
            else:
                return Response(form.errors,status=400)
        
        
    

class ObjectsDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Objectss.objects.all()
    serializer_class = ObjectsSerializer
               
        
class UsertDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class CommentAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
 
 
class MINISTOPViewSet(ModelViewSet):
    queryset = MINISTOP.objects.all()
    serializer_class = MinistopSerializer   
    
    filter_backends = [SearchFilter]
    search_fields = ['name']
    
    @action(detail=False, methods=['get'])
    def typesearch(self,request):
        if self.request.query_params.get('search')==None:
            paginator = PageNumberPagination()
            paginator.page_size = 20
            queryset = MINISTOP.objects.filter(type=self.request.query_params.get('data'))
            result_page = paginator.paginate_queryset(queryset, request)
            serializer = MinistopSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            paginator = PageNumberPagination()
            paginator.page_size = 20
            search = self.request.query_params.get('search')
            queryset = MINISTOP.objects.filter(type=self.request.query_params.get('data'),name__contains=search)
            result_page = paginator.paginate_queryset(queryset, request)
            serializer = MinistopSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
    
class Gs25ViewSet(ModelViewSet):
    queryset = GS25.objects.all()
    serializer_class = Gs25Serializer
    
    filter_backends = [SearchFilter]
    search_fields = ['name']
    
    @action(detail=False, methods=['get'])
    def typesearch(self,request):
        if self.request.query_params.get('search')==None:
            paginator = PageNumberPagination()
            paginator.page_size = 20
            queryset = GS25.objects.filter(type=self.request.query_params.get('data'))
            result_page = paginator.paginate_queryset(queryset, request)
            serializer = Gs25Serializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            paginator = PageNumberPagination()
            paginator.page_size = 20
            search = self.request.query_params.get('search')
            queryset = GS25.objects.filter(type=self.request.query_params.get('data'),name__contains=search)
            result_page = paginator.paginate_queryset(queryset, request)
            serializer = Gs25Serializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
    
class CUViewSet(ModelViewSet):
    queryset = CU.objects.all()
    serializer_class = CuSerializer 
    
    filter_backends = [SearchFilter]
    search_fields = ['name']
    
    @action(detail=False, methods=['get'])
    def typesearch(self,request):
        if self.request.query_params.get('search')==None:
            paginator = PageNumberPagination()
            paginator.page_size = 20
            queryset = CU.objects.filter(type=self.request.query_params.get('data'))
            result_page = paginator.paginate_queryset(queryset, request)
            serializer = CuSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            paginator = PageNumberPagination()
            paginator.page_size = 20
            search = self.request.query_params.get('search')
            queryset = CU.objects.filter(type=self.request.query_params.get('data'),name__contains=search)
            result_page = paginator.paginate_queryset(queryset, request)
            serializer = CuSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        
class BlacklistRefreshView(APIView):
    def post(self, request):
        token = RefreshToken(request.data.get('refresh'))
        token.blacklist()
        return Response(status=status.HTTP_200_OK)
    
