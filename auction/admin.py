from django.contrib import admin

from .models import Post, PostImage, Bet


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(PostImage)
class PostImagesAdmin(admin.ModelAdmin):
    pass


@admin.register(Bet)
class BetAdmin(admin.ModelAdmin):
    pass
