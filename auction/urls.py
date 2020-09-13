from django.urls import path

from .views import (
    PostsList, PostDetail, make_bet
)

urlpatterns = [
    path("", PostsList.as_view(), name="post-list"),
    path("post/<int:pk>/", PostDetail.as_view(), name="post-detail"),
    path("post/<int:pk>/make_bet/", make_bet, name="make-bet")
]
