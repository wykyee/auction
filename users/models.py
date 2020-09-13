from django.contrib.auth.models import AbstractUser
from django.db import models


class Profile(AbstractUser):
    """
    Custom user model that has data about profile
    """
    avatar = models.ImageField(
        upload_to='users/avatars/', null=True, blank=True
    )
    info = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'Profile'

    def __str__(self) -> str:
        return f'{self.id}:{self.username}'

    def delete(self, *args, **kwargs) -> None:
        """
        Removes file from media root, when it is removed from db.
        """
        self.avatar.delete()
        super().delete(*args, **kwargs)

