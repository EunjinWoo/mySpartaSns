from django.shortcuts import render, redirect
# render라는 걸 통해서 html 파일을 화면에 보여질 수 있도록 함.
from .models import UserModel
# 내 위치와 동일한 친구 중 models를 가져올 건데, 그 모델 중에서 UserModel이라는 애를 가져오겠다.
from django.http import HttpResponse # 화면에 글자 띄울 때 활용.
from django.contrib.auth import get_user_model # 사용자가 데이터베이스 안에 있는지 검사하는 함수.
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# Create your views here.
def sign_up_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated # 인증된 사용자를 user라는 변수에 입력
        if user:
            return redirect('/')
        else:
            return render(request, 'user/signup.html')
    elif request.method == 'POST':
        # 전체적으로 DB에 저장하는 기능

        username = request.POST.get('username', '') # post로 온 데이터 중 username이라는 이름으로 된 데이터를 가져오고 싶다. 만약 username이 없다면, None으로, 빈칸으로 처리하겠다.라는 것.
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        bio = request.POST.get('bio', '')


        if password != password2:
            return render(request, 'user/signup.html', {'error':'패스워드를 확인해주세요.'}) # 해당하는 화면을 다시 보여줄 것. 비번 확인 오류로 저장이 되면 안되기 때문에.
        else:
            exist_user = get_user_model().objects.filter(username=username)
            if exist_user:
                return render(request, 'user/signup.html', {'error': '같은 이름의 사용자가 존재합니다.'})
            if username == '' or password == '':
                return render(request, 'user/signup.html', {'error': '사용자 이름과 비밀번호는 필수 값입니다.'})
            # ----- 장고 기본 기능 이용 안하고 만든 것 -------
            # new_user = UserModel()
            # new_user.username = username
            # new_user.password = password
            # new_user.bio = bio
            #
            # new_user.save() # 위에 적은 정보들을 DB에 저장.

            # --------- 장고 기본 기능 이용 -------------
            UserModel.objects.create_user(username=username, password=password, bio=bio)

        # 저장이 된 후에 로그인 화면이 보이게끔 함.
        return redirect('/sign-in')


def sign_in_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        me = auth.authenticate(request, username=username, password=password)
        # 인증기능 모듈 auth를 먼저 불러오고, authenticate이라는 기능을 이용해 암호화된 비번과 현재 입력된 비번이 맞는지, 그게 사용자와 맞는지 까지 한 번에 해 줌.

        # ----- 장고 기본 기능 이용 안하고 만든 것 -------
        # me = UserModel.objects.get(username=username) # UserModel은 이미 DB와 연결되어있는 클래스. 여기서 어떤 데이터를 가져올 건지 써준 거. 왼쪽의 빨간색 username은 UserModel 클래스 내의 변수인 username임. 그래서 이 변수가 위의 username인 사람을 가져오고 싶다.라는 것.

        # if me.password == password:
        if me is not None:
            # ----- 장고 기본 기능 이용 안하고 만든 것 -------
            # session : 사용자 정보를 저장할 수 있는 공간.
            # request.session['user'] = me.username

            # --------- 장고 기본 기능 이용 -------------
            auth.login(request, me)

            return redirect('/')
        else:
            return render(request, 'user/signin.html', {'error':'유저이름 혹은 패스워드를 확인해주세요.'})

    elif request.method == 'GET':
        user = request.user.is_authenticated  # 인증된 사용자를 user라는 변수에 입력
        if user:
            return redirect('/')
        else:
            return render(request, 'user/signin.html')

@login_required # 로그인 된 상태여야먄 접근이 가능한 함수라는 뜻.
def logout(request):
    auth.logout(request)
    return redirect('/')

# user/views.py

@login_required
def user_view(request):
    if request.method == 'GET':
        # 사용자를 불러오기, exclude와 request.user.username 를 사용해서 '로그인 한 사용자'를 제외하기
        user_list = UserModel.objects.all().exclude(username=request.user.username)
        return render(request, 'user/user_list.html', {'user_list': user_list})


@login_required
def user_follow(request, id):
    me = request.user
    click_user = UserModel.objects.get(id=id)
    if me in click_user.followee.all():
        click_user.followee.remove(request.user)
    else:
        click_user.followee.add(request.user)
    return redirect('/user')