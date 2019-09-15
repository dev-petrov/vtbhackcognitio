from django.contrib import admin

from .models import Document, Result, Comment, User

# Register your models here.
admin.site.register(Document)
admin.site.register(Result)
admin.site.register(Comment)
admin.site.register(User)

