from django.conf.urls import url,include
from django.contrib import admin
from online import models,views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.login, name='login'),
    url(r'^login/$', views.login, name='login'),
    url(r'^regist/$', views.regist, name='regist'),
    url(r'^login_success/$', views.login_success, name='login_success'),
    #url(r'^logout/$', views.login, name='logout'),
]