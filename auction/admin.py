from django.contrib import admin

from .models import Post, PostImages, Bet


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(PostImages)
class PostImagesAdmin(admin.ModelAdmin):
    pass


@admin.register(Bet)
class BetAdmin(admin.ModelAdmin):
    pass
