from django.contrib import admin
from online.models import User
from online.models import UserRelationship
from online.models import UserBlocked
admin.site.register(User)
admin.site.register(UserRelationship)
admin.site.register(UserBlocked)
# Register your models here.
