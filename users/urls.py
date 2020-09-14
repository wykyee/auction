from django.urls import path

from users.views import ProfileView, ChangeProfileView

urlpatterns = [
    path("", ProfileView.as_view(), name="profile-data"),
    path("change_data/", ChangeProfileView.as_view(), name="profile-change"),
]
