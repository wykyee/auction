from django.shortcuts import redirect
from django.views.generic import ListView, DetailView

from .forms import BetForm
from .models import Post
from .services import get_all_active_posts, get_post_by_pk


class PostsList(ListView):
    # TODO: current_bet needed in the context
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

        try:
            context["current_bet"] = post_instance.bets.last().amount
        except AttributeError:
            context["current_bet"] = post_instance.initial_bet
        context["form"] = BetForm()
        return context


def make_bet(request, pk):
    # TODO: raise form.ValidationError if amount not in limits or smthing like that to see errors
    if request.method == "POST":
        certain_post = get_post_by_pk(pk)
        try:
            current_bet = certain_post.bets.last().amount
        except AttributeError:
            current_bet = certain_post.initial_bet
        amount = int(request.POST['amount'])

        if current_bet < amount < certain_post.permanent_price:
            form = BetForm(data=request.POST,
                           better=request.user,
                           post=certain_post)
            if form.is_valid():
                form.save()
                return redirect('post-detail', pk=pk)
        else:
            return redirect('post-detail', pk=pk)
    else:
        return redirect("post-list")
