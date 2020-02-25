# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django import forms
from online.models import User
from online.models import UserRelationship
from online.models import UserBlocked
import re
def contextOfHomepage(error):
    username = req.COOKIES.get('username', '')
    friendList = friendsOf(username)
    blockList = BeBlockedBy(username)
    context = {'error':error, 'username': username, 'friendList': friendList,'blockList': blockList}
    return context
    
def friendsOf(username):
    friends = UserRelationship.objects.filter(selfname__exact=username)
    friendList = ''
    for friend in friends:
        friendList = friendList + '\n' + '\'' + friend.friendname + '\''
    return friendList

def BeBlockedBy(username):
    friends = UserBlocked.objects.filter(selfname__exact=username)
    friendList = ''
    for friend in friends:
        friendList = friendList + '\n' + '\'' + friend.blockname + '\''
    return friendList
# 表单 from
class RegistUserForm(forms.Form):
    username = forms.CharField(label='username', max_length=100)
    password = forms.CharField(label='password', widget=forms.PasswordInput())
    mail = forms.CharField(label='mail', max_length=100)
    fullname = forms.CharField(label='fullname', max_length=100)


class AddFriendForm(forms.Form):
    friendWaitToAdd = forms.CharField(label='friendWaitToAdd', max_length=100)


class DeleteFriendForm(forms.Form):
    friendWaitToDelete = forms.CharField(label='friendWaitToDelete', max_length=100)
class BlockFriendForm(forms.Form):
    friendWaitToBlock = forms.CharField(label='friendWaitToDelete', max_length=100)

class LoginUserForm(forms.Form):
    username = forms.CharField(label='username', max_length=100)
    password = forms.CharField(label='password', widget=forms.PasswordInput())


# 注册regiser
def register(req):
    if req.method == 'POST':
        uf = RegistUserForm(req.POST)
        if uf.is_valid():
            # 获得表单数据 get data form form
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            mail = uf.cleaned_data['mail']
            fullname = uf.cleaned_data['fullname']
            # 添加到数据库 insert to databse
            filterResult = User.objects.filter(username=username)
            if len(filterResult) > 0:
                context = {'error': 'Existed usename'}
                return render(req, 'regist.html', context)
            else:
                t_or_f = re.search(r"\W", password)
                if t_or_f == None or len(password) < 8:
                    context = {'error': 'password be at least 8 characters long with a special character'}
                    return render(req, 'regist.html', context)
                else:
                    User.objects.create(username=username, password=password, mail=mail, fullname=fullname)
                    return render(req, 'regist_success.html')
    else:
        uf = RegistUserForm()
    return render(req, 'regist.html', {'uf': uf})


# 登陆 login
def login(req):
    if req.method == 'POST':
        uf = LoginUserForm(req.POST)
        if uf.is_valid():
            # 获取表单用户密码 get username and password from form
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            # 获取的表单数据与数据库进行比较 compare data of form with database
            user = User.objects.filter(username__exact=username, password__exact=password)
            if user:
                # 比较成功，跳转= ;  if success ,jump to
                response = HttpResponseRedirect('/online/userHomepage/')
                # 将username写入浏览器cookie,失效时间为3600
                response.set_cookie('username', username, 3600)
                return response
            else:
                # 比较失败，还在login ;if fail ,stay  in login
                context = {'error': 'wrong password'}
                return render(req, 'login.html', context)
            # return HttpResponseRedirect('/online/login/')
    else:
        uf = LoginUserForm()
    return render(req, 'login.html', {'uf': uf})


# 登陆成功  when success , turn to user homepage


#   else:
#      aff = AddFriendForm()
#  return render(req,'userHomepage',{'aff':aff})

# 退出
def logout(req):
    response = HttpResponse('logout !!')
    response.delete_cookie('username')
    return render(req, 'login.html')
def userHomepage(req):
    username = req.COOKIES.get('username', '')
    friendList = friendsOf(username)
    blockList = BeBlockedBy(username)
    if req.method == 'POST':
        if 'add' in req.POST:
            aff = AddFriendForm(req.POST)
            if aff.is_valid():
                friendWaitToAdd = aff.cleaned_data['friendWaitToAdd']
                isRelationExist = UserRelationship.objects.filter(selfname__exact=username,
                                                                  friendname__exact=friendWaitToAdd)
                isfFiendWaitToAddExist = User.objects.filter(username__exact=friendWaitToAdd)
                if not isfFiendWaitToAddExist:
                    context = {'error': 'friendWaitToAdd is not exist', 'username': username, 'friendList': friendList,
                               'blockList': blockList}
                    #context=contextOfHomepage( 'friendWaitToAdd is not exist')
                    return render(req, 'userHomepage.html', context)
                else:
                    if isRelationExist:
                        context = {'error1': req.method, 'error': 'friendWaitToAdd is  already your friend',
                                   'username': username, 'friendList': friendList, 'blockList': blockList}
                        return render(req, 'userHomepage.html', context)
                    else:
                        UserRelationship.objects.create(selfname=username, friendname=friendWaitToAdd)
                        friendList = friendsOf(username)
                        context = {'error': 'done', 'username': username, 'friendList': friendList,
                                   'blockList': blockList}
                        return render(req, 'userHomepage.html', context)
            else:
                context = {'username': username, 'friendList': friendList, 'blockList': blockList}
                return render(req, 'userHomepage.html', context)

        elif 'delete' in req.POST:
            dff = DeleteFriendForm(req.POST)
            if dff.is_valid():
                friendWaitToDelete = dff.cleaned_data['friendWaitToDelete']
                isRelationExist = UserRelationship.objects.filter(selfname__exact=username,
                                                                  friendname__exact=friendWaitToDelete)
                isfFiendWaitToDelete = User.objects.filter(username__exact=friendWaitToDelete)
                if not isfFiendWaitToDelete:
                    context = {'error': 'friendWaitToDelete is not exist', 'username': username,
                               'friendList': friendList, 'blockList': blockList}
                    return render(req, 'userHomepage.html', context)
                else:
                    if not isRelationExist:
                        context = {'error': 'friendWaitToDelete is not your friend', 'username': username,
                                   'friendList': friendList, 'blockList': blockList}
                        return render(req, 'userHomepage.html', context)
                    else:
                        UserRelationship.objects.filter(selfname=username, friendname=friendWaitToDelete).delete()
                        friends = UserRelationship.objects.filter(selfname__exact=username)
                        friendList = ''
                        for friend in friends:
                            friendList = friendList + '\n' + '\'' + friend.friendname + '\''
                        context = {'error': 'done', 'username': username, 'friendList': friendList,
                                   'blockList': blockList}
                        return render(req, 'userHomepage.html', context)
            else:
                context = {'username': username, 'friendList': friendList, 'blockList': blockList}
                return render(req, 'userHomepage.html', context)
        elif 'block' in req.POST:
            bff = BlockFriendForm(req.POST)
            if bff.is_valid():
                friendWaitToBlock = bff.cleaned_data['friendWaitToBlock']
                isRelationExist = UserBlocked.objects.filter(selfname__exact=username,
                                                             blockname__exact=friendWaitToBlock)
                isfFiendWaitToBlock = User.objects.filter(username__exact=friendWaitToBlock)
                if not isfFiendWaitToBlock:
                    context = {'error': 'friendWaitToBlock is not exist', 'username': username,
                               'friendList': friendList, 'blockList': blockList}
                    return render(req, 'userHomepage.html', context)
                else:
                    if isRelationExist:
                        context = {'error': 'already blocked', 'username': username, 'friendList': friendList,'blockList': blockList}
                        return render(req, 'userHomepage.html', context)
                    else:
                        UserBlocked.objects.create(selfname=username, blockname=friendWaitToBlock)
                        blockList = BeBlockedBy(username)
                        context = {'error': 'done', 'username': username, 'friendList': friendList,
                                   'blockList': blockList}
                        return render(req, 'userHomepage.html', context)
            else:
                context = {'username': username, 'friendList': friendList, 'blockList': blockList}
                return render(req, 'userHomepage.html', context)

    else:
        context = {'username': username, 'friendList': friendList, 'blockList': blockList}
        return render(req, 'userHomepage.html', context)

