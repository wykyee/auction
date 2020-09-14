from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView

from .forms import BetForm
from .services import (
    get_all_active_posts, get_post_by_pk, get_current_bet_for_post
)


class PostsList(ListView):
    context_object_name = "posts"
    template_name = "auction/post_list.html"
    queryset = get_all_active_posts()


class PostDetail(DetailView):
    context_object_name = "post"
    template_name = "auction/post_detail.html"
    queryset = get_all_active_posts()

    def get_context_data(self, **kwargs) -> dict:
        context = super(PostDetail, self).get_context_data()
        post_instance = context["post"]

        context["current_bet"] = get_current_bet_for_post(post_instance)
        context["form"] = BetForm()
        return context


def make_bet(request: HttpRequest, pk: int) -> HttpResponse:
    if request.method == "POST":
        certain_post = get_post_by_pk(pk)
        current_bet = get_current_bet_for_post(certain_post)

        form = BetForm(data=request.POST,
                       better=request.user,
                       post=certain_post,
                       current_bet=current_bet)
        if form.is_valid():
            form.save()
            return redirect("post-detail", pk=pk)
        else:
            context = {
                "form": form,
                "post": certain_post,
                "current_bet": current_bet,
            }
            return render(request, "auction/post_detail.html", context=context)
    else:
        return redirect("post-detail", pk=pk)
