"""DRF URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter
from .views import * 
from rest_framework_simplejwt.views import TokenVerifyView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

router = DefaultRouter()
router.register('',views.MainPostsViewSet)
router.register('event/GS25',views.Gs25ViewSet)
router.register('event/MINISTOP',views.MINISTOPViewSet)
router.register('event/CU',views.CUViewSet)


urlpatterns = [
    
    path('Main/',include(router.urls)),
    
    path('best/', views.BestAPIView.as_view()),
    
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    path('posts/', views.PostsAPIView.as_view()),
    path('posts/<int:pk>',views.PostsDetailAPIView.as_view()),
    
    path('comment/', views.CommentAPIView.as_view()),
    path('comment/<int:pk>/', views.CommentDetailAPIView.as_view()),
    
    path('user/', views.UserAPIView.as_view()),
    path('user/ReEmail/', views.ReEmailTest.as_view()),
    path('user/<int:pk>/', views.UsertDetailAPIView.as_view()),
    path('user/logout/',views.BlacklistRefreshView.as_view()),
    
    path('user/passwdfind/', views.UserPasswdFind.as_view()),
    path('user/idfind/', views.UserIdFind.as_view()),
    
    path('OverLapEmail/', views.OverLapEmail.as_view()),
    path('OverLapNickname/', views.OverLapNickname.as_view()),
    
    path('board/', views.BoardAPIView.as_view()),
    path('board/<int:pk>/', views.BoardDetailAPIView.as_view()),
    
    path('boardcomment/', views.BoardCommentAPIView.as_view()),
    path('boardcomment/<int:pk>/', views.BoardCommentDetailAPIView.as_view()),
    
    
    path('objects/', views.ObjectsAPIView.as_view()),
    path('objects/<int:pk>/', views.ObjectsDetailAPIView.as_view()),
    
    path('objectssearch/', views.ObjectsPostsSearch.as_view()),
    
    path('accounts/activate/<str:uidb64>/<str:token>', Activate.as_view()),
    path('accounts/passwd/<str:uidb64>/<str:token>', PasswdFind.as_view()),
    path('accounts/passwd/changetest/', PasswdFind.as_view()),
    path('accounts/', include('dj_rest_auth.urls')),
    path('accounts/', include('dj_rest_auth.registration.urls')),
    path('accounts/', include('allauth.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)