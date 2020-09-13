from typing import Union

from django.db.models import QuerySet

from auction.models import Post


def get_all_active_posts() -> QuerySet:
    """
    Returns all active posts.
    """
    return Post.objects.filter(is_active=True)


def get_post_by_pk(pk: int) -> Union[Post, None]:
    """
    Returns post by pk
    """
    try:
        return Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return None
