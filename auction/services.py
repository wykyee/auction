from django.db.models import QuerySet

from auction.models import Post


def get_all_active_posts() -> QuerySet:
    """
    Returns all active posts.
    """
    return Post.objects.filter(is_active=True)
