from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)

from .forms import BetForm, PostSortForm, PostCreateForm, PostUpdateForm
from .mixins import AuthorRequiredMixin
from .models import Post
from .services import (
    get_all_active_posts, get_post_by_pk, get_current_bet_for_post
)


class PostsList(ListView):
    context_object_name = "posts"
    template_name = "auction/post_list.html"

    def get_context_data(self, **kwargs) -> dict:
        context = super(PostsList, self).get_context_data(**kwargs)
        context["sort_form"] = PostSortForm()
        return context

    def get_queryset(self) -> QuerySet:
        qs = get_all_active_posts()
        price_sort = self.request.GET.get("price", "")
        created_sort = self.request.GET.get("created", "")
        author = self.request.GET.get("author", "")
        order = []
        if author:
            qs = qs.filter(author__username=author)

        if price_sort == "from_cheapest":
            order.append("permanent_price")
        else:
            order.append("-permanent_price")

        if created_sort == "from_newest":
            order.append("-created_at")
        else:
            order.append("created_at")
        qs = qs.order_by(*order)

        return qs


class PostDetail(DetailView):
    context_object_name = "post"
    template_name = "auction/post_detail.html"
    queryset = get_all_active_posts()

    def get_context_data(self, **kwargs) -> dict:
        context: dict = super(PostDetail, self).get_context_data()
        post_instance = context["post"]

        if self.request.user.is_authenticated:
            context["form"] = BetForm()
        if self.request.user.is_superuser or self.request.user == post_instance.author:
            context["can_modify"] = True
        return context


@login_required
def make_bet(request: HttpRequest, pk: int) -> HttpResponse:
    if request.method == "POST":
        certain_post: Post = get_post_by_pk(pk)
        current_bet: int = get_current_bet_for_post(certain_post)

        form = BetForm(data=request.POST,
                       better=request.user,
                       post=certain_post,
                       current_bet=current_bet)
        if form.is_valid():
            form.save()
            return redirect("post-detail", pk=pk)

    return redirect("post-detail", pk=pk)


class PostCreate(LoginRequiredMixin, CreateView):
    template_name = "auction/post_create.html"

    def get_success_url(self) -> str:
        return reverse_lazy("post-detail", kwargs={"pk": self.object.pk})

    def get_form(self, **kwargs) -> PostCreateForm:
        author = self.request.user
        return PostCreateForm(**self.get_form_kwargs(), author=author)


class PostUpdate(AuthorRequiredMixin, UpdateView):
    template_name = 'auction/post_update.html'

    def get_object(self, **kwargs) -> Post:
        return get_post_by_pk(self.kwargs["pk"])

    def get_form(self, **kwargs) -> PostUpdateForm:
        author = self.request.user
        return PostUpdateForm(**self.get_form_kwargs(), author=author)


class PostDelete(AuthorRequiredMixin, DeleteView):
    model = Post
    template_name = "auction/post_delete.html"
    success_url = reverse_lazy("post-list")

