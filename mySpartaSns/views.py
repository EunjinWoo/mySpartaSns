from django.http import HttpResponse
from django.shortcuts import render

def base_response(request):
    return HttpResponse("안녕하세요! 장고의 시작입니다!") # HttpResponse : 괄호 안의 내용을 전달하는 애.

def first_view(request): # my_test.html을 보여주는 역할을 하는 함수.
    return render(request, 'my_test.html')