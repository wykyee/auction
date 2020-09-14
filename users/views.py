from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView
from django.views.generic.base import View

from users.services import (
    get_all_available_users, get_user_from_pk
)


Profile = get_user_model()


class BetsList(ListView):
    pass


class ProfileView(View):
    @staticmethod
    def get(request: HttpRequest) -> HttpResponse:
        context = {
            "user": request.user,
        }
        return render(request, "users/profile_data.html", context=context)


class ChangeProfileView(UpdateView):
    template_name = "users/change_profile_data.html"
    model = Profile
    fields = ("avatar", "first_name",
              "last_name", "email",
              "birthdate", "info",)
    success_url = reverse_lazy("profile-data")
    # TODO: add password change
    def get_object(self, **kwargs):
        return get_user_from_pk(pk=self.request.user.pk)
