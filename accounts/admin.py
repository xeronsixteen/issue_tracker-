# Register your models here.
from django.contrib.auth import get_user_model
from django.contrib import admin

from accounts.models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile


class UserAdmin(admin.ModelAdmin):
    inlines = (ProfileInline,)


admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), UserAdmin)
