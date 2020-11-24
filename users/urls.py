from django.urls import path

from users.views import (
    ProfileDetailView, ProfileChangeView, ProfileLoginView, ProfileLogoutView,
    ProfileRegisterView, ProfileChangePasswordView
)

urlpatterns = [
    path("", ProfileDetailView.as_view(), name="profile-data"),
    path("change_data/", ProfileChangeView.as_view(), name="profile-change"),
    path("login/", ProfileLoginView.as_view(), name="profile-login"),
    path("register/", ProfileRegisterView.as_view(), name="profile-register"),
    path("logout/", ProfileLogoutView.as_view(), name="profile-logout"),
    path("change_password/", ProfileChangePasswordView.as_view(), name="change-password"),
]
