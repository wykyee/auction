from django.contrib.auth import get_user_model, logout, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView
from django.views.generic.base import View, RedirectView

from users.forms import LoginForm, ProfileForm, ProfileRegisterForm
from users.services import (
    get_user_from_pk
)

Profile = get_user_model()


class BetsList(ListView):
    pass


class ProfileDetailView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "user": request.user,
        }
        return render(request, "users/profile_detail.html", context=context)


class ProfileRegisterView(CreateView):
    template_name = "users/register.html"
    form_class = ProfileRegisterForm

    def form_valid(self, form):
        """
        Automatically login after registration.
        """
        form.save()
        username = self.request.POST['username']
        password = self.request.POST['password']
        profile = authenticate(username=username, password=password)
        login(self.request, profile)

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self) -> str:
        return reverse_lazy('post-list')


class ProfileChangeView(UpdateView):
    template_name = "users/profile_update.html"
    form_class = ProfileForm
    success_url = reverse_lazy("profile-data")

    def get_object(self, **kwargs):
        return get_user_from_pk(pk=self.request.user.pk)


class ProfileLoginView(LoginView):
    template_name = "users/login.html"
    authentication_form = LoginForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('post-list')
        return self.render_to_response(self.get_context_data())

    def get_success_url(self) -> str:
        next_url: str = self.request.META.get('QUERY_STRING')
        if next_url and next_url[:5] == 'next=':
            return next_url[5:]
        return reverse_lazy('post-list')


class ProfileLogoutView(LoginRequiredMixin, RedirectView):
    url = reverse_lazy('post-list')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)

