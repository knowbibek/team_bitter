from django.conf.urls import url,include
from django.contrib import admin
from online import models,views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.login, name='login'),
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^userHomepage/$', views.userHomepage, name='userHomepage'),
    #url(r'^logout/$', views.login, name='logout'),
]