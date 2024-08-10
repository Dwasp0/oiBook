from django.contrib import admin

from .models import Page, Comment, Exercise

# Register your models here.

admin.site.register(Page)
admin.site.register(Comment)
admin.site.register(Exercise)