from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(User_profile)
admin.site.register(User_post)
admin.site.register(Post_like)
admin.site.register(Post_comment)
admin.site.register(Text_post)
admin.site.register(Photo_post)

admin.site.register(Audio_post)
admin.site.register(Video_post)
admin.site.register(Friendship_request)
admin.site.register(Follow_request)