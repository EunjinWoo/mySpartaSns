#user/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
# AbstractUser : 장고가 제공하는 auth_user라는 테이블과 연동되는 class.
from django.conf import settings


# Create your models here.
class UserModel(AbstractUser): # 우리가 생성한 클래스의 이름
    class Meta: # DB table의 이름을 지정해주는 정보.
        db_table = "my_user"

    bio = models.CharField(max_length=256, default='')
    # 장고의 기본적인 모델을 사용하고, 우리가 추가적으로 bio라는 걸 추가해줬다. 라는 것.
    follow = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followee')