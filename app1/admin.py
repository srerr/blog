from django.contrib import admin
from django.contrib.auth.models import User
from app1.models import Post,Tag,Comments,Profile,WebsiteMeta
# Register your models here.
admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Comments)
admin.site.register(Profile)
#admin.site.register(WebsiteMeta)
