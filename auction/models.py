from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

Profile = get_user_model()


class Post(models.Model):
    """
    Model for representing post with info of car.
    """
    title = models.CharField("Название", max_length=120)
    permanent_price = models.PositiveIntegerField()
    initial_bet = models.PositiveIntegerField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    main_image = models.ImageField(upload_to="auction/images")

    class Meta:
        db_table = "Post"
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.title}"

    def get_absolute_url(self) -> str:
        return reverse("post-detail", args=[self.pk])


class PostImage(models.Model):
    """
    Model for representing images of the posts.
    """
    image = models.ImageField(
        upload_to="auction/images/", blank=True, null=True
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Картинка к посту"
        verbose_name_plural = "Картинки к постам"


class Bet(models.Model):
    """
    Model for representing of bet of certain user for certain post.
    """
    amount = models.PositiveIntegerField()
    better = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='bets'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Bet"
        verbose_name = "Ставка"
        verbose_name_plural = "Ставки"

    def __str__(self) -> str:
        return f"BET OF {self.better} TO POST {self.post.title}; " \
               f"AMOUNT {self.amount}"
