from django.views.generic import ListView, DetailView

from .services import get_all_active_posts


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
        try:
            context["current_bet"] = context["post"].bets.last().amount
        except AttributeError:
            context["current_bet"] = context["post"].initial_bet

        return context
