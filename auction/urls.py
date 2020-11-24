from django.urls import path, reverse
from django.views.generic import RedirectView

from .views import (
	PostsList, PostDetail, make_bet, PostCreate, PostDelete, PostUpdate
)

urlpatterns = [
	path("", RedirectView.as_view(pattern_name='post-list')),
	path("posts", PostsList.as_view(), name="post-list"),
	path("post/<int:pk>/", PostDetail.as_view(), name="post-detail"),
	path("post/create/", PostCreate.as_view(), name="post-create"),
	path("post/<int:pk>/update/", PostUpdate.as_view(), name="post-update"),
	path("post/<int:pk>/delete/", PostDelete.as_view(), name="post-delete"),
	path("post/<int:pk>/make_bet/", make_bet, name="make-bet"),
]
