from django.contrib.auth import get_user_model
from django.db import models


Profile = get_user_model()


class Post(models.Model):
    title = models.CharField("Название", max_length=120)
    permanent_price = models.PositiveIntegerField()
    current_bet = models.PositiveIntegerField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)

    class Meta:
        db_table = "Post"

    def __str__(self) -> str:
        return f"{self.title}"

    def get_absolute_url(self) -> str:
        # TODO
        return f""


class PostImages(models.Model):
    """ Model for representing images of the posts."""
    image = models.ImageField(
        upload_to="auction/images/", blank=True, null=True
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Bet(models.Model):
    """
    Model for representing of bet of certain user for certain post.
    """
    amount = models.PositiveIntegerField()
    better = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.better} TO POST {self.post.id}. UAH: {self.amount}"
