from django.contrib.auth import get_user_model
from django.db.models import QuerySet


Profile = get_user_model()


def get_all_available_users() -> QuerySet:
    return Profile.objects.filter(is_active=True)


def get_user_from_pk(pk) -> Profile:
    return Profile.objects.get(pk=pk)
