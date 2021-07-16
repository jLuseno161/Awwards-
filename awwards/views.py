from django.http.response import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='/accounts/login/')
def index(request):
 
  
    return HttpResponse('Hi there my name is Joy')
