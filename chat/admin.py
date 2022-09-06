from django.contrib import admin
from .models import UserProfile, chatMessages, UploadFile, FeedFile, Writehelp, WhiteHelpFile

admin.site.register(UserProfile)
admin.site.register(chatMessages)
admin.site.register(UploadFile)
admin.site.register(FeedFile)
admin.site.register(Writehelp)
admin.site.register(WhiteHelpFile)