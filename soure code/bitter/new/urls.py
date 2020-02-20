from django.conf.urls import url,include
from django.contrib import admin
from online import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
   url(r'^online/', include('online.urls')),

]