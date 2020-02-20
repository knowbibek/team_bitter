# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django import forms
from online.models import User
import re

#表单
class RegistUserForm(forms.Form):
    username = forms.CharField(label='username',max_length=100)
    password = forms.CharField(label='password',widget=forms.PasswordInput())
    mail = forms.CharField(label='mail',max_length=100)
    fullname = forms.CharField(label='fullname',max_length=100)

class LoginUserForm(forms.Form):
    username = forms.CharField(label='username',max_length=100)
    password = forms.CharField(label='password',widget=forms.PasswordInput())
#注册
def regist(req):
    if req.method == 'POST':
        uf =RegistUserForm(req.POST)
        if uf.is_valid():
            #获得表单数据
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            mail = uf.cleaned_data['mail']
            fullname = uf.cleaned_data['fullname']
            #添加到数据库
            filterResult=User.objects.filter(username=username)
            if len(filterResult)>0:
                context={'error':'Existed usename'}
                return  render(req,'regist.html',context)
            else:
                t_or_f= re.search(r"\W",password)
                if t_or_f==None or len(password)<8:
                    context={'error':'password be at least 8 characters long with a special character'}
                    return  render(req,'regist.html',context)
                else:
                    User.objects.create(username= username,password=password,mail=mail,fullname=fullname)
                    return render(req,'regist_success.html')
    else:
        uf = RegistUserForm()
    return render(req,'regist.html',{'uf':uf})

#登陆
def login(req):
    if req.method == 'POST':
        uf = LoginUserForm(req.POST)
        if uf.is_valid():
            #获取表单用户密码
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            #获取的表单数据与数据库进行比较
            user = User.objects.filter(username__exact = username,password__exact = password)
            if user:
                #比较成功，跳转index
                response = HttpResponseRedirect('/online/login_success/')
                #将username写入浏览器cookie,失效时间为3600
                response.set_cookie('username',username,3600)
                return response
            else:
                #比较失败，还在login
                context={'error':'wrong password'}
                return  render(req,'login.html',context)
               # return HttpResponseRedirect('/online/login/')
    else:
        uf = LoginUserForm()
    return render(req,'login.html',{'uf':uf})

#登陆成功
def login_success(req):
    username = req.COOKIES.get('username','')
    return render(req,'login_success.html' ,{'username':username})

#退出
def logout(req):
    response = HttpResponse('logout !!')
    response.delete_cookie('username')
    return render(req,'login.html')