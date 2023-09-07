from django.urls import path
from . import views # 작성한 views.py를 urls.py에 연결해 주기

urlpatterns = [
    # 앞의 url로 접근하면, views."함수" 가 실행이 되면서 그 함수에 담긴 html 파일이 보여질 것.
    path('sign-up/', views.sign_up_view, name='sign-up'),
    path('sign-in/', views.sign_in_view, name='sign-in'),
    path('logout/', views.logout, name='logout'),
    path('user/', views.user_view, name='user-list'),
    path('user/follow/<int:id>', views.user_follow, name='user-follow'),
]