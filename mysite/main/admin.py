from django.contrib import admin
from .models import Tutorial
from tinymce.widgets import TinyMCE
from django.db import models


class TutorialAdmin(admin.ModelAdmin):
    fields = ["tutorial_title",
              "tutorial_published",
              "tutorial_content"
    ]

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
        }


# Register your models here.
admin.site.register(Tutorial, TutorialAdmin)