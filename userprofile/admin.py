from django.contrib import admin

from userprofile.models import UserProfile, SocialAccount


class UserProfileAdmin(admin.ModelAdmin):
    pass


class SocialAccountAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(SocialAccount, SocialAccountAdmin)
