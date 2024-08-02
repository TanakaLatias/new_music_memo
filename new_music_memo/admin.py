from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import User, Song, Scene, Poll, Post, Like, Listened
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin

class UserAdmin(UserAdmin):
    list_display = ('pk', 'username', 'email')
    ordering = ('-pk',)

class SongAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'singer')
    search_fields = ('title', 'singer')
    ordering = ('-pk',)

class SceneAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'song')
    search_fields = ('title', 'song__title__icontains', 'user__email__icontains')
    ordering = ('-pk',)

class PollAdmin(admin.ModelAdmin):
    list_display = ('pk', 'scene', 'user')
    search_fields = ('scene__song__title__icontains', 'user__email__icontains')
    ordering = ('-pk',)

class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'song', 'user', 'hide')
    search_fields = ('song__title__icontains', 'user__email__icontains')
    ordering = ('-pk',)

class LikeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'post')
    search_fields = ('user__email__icontains', 'post__work__title__icontains')
    ordering = ('-pk',)

class ListenedAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'song')
    search_fields = ('song__title__icontains', 'user__email__icontains')
    ordering = ('-pk',)

admin.site.register(Song, SongAdmin)
admin.site.register(Scene, SceneAdmin)
admin.site.register(Poll, PollAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Listened, ListenedAdmin)
admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)