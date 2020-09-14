from django import forms
from django.utils.translation import ugettext_lazy as _

from auction.models import Bet


class BetForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        """
        Gets author for initial parameter to save it as author of post.
        """
        self.better = kwargs.pop('better', None)
        self.post = kwargs.pop('post', None)
        self.current_bet = kwargs.pop('current_bet', None)
        super(BetForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Bet
        fields = ["amount", ]
        labels = {
            "amount": _("Количество"),
        }

    def clean_amount(self) -> int:
        """
        Checks if input amount is in limits.
        """
        data = self.cleaned_data["amount"]

        if self.current_bet >= data or data >= self.post.permanent_price:
            self.add_error("amount", _("Введите валидное значение"))

        return data

    def save(self, commit=True):
        """
        Saves user from request automatically as better and
        post from init as post instance.
        """
        bet = super(BetForm, self).save(commit=False)
        bet.better = self.better
        bet.post = self.post
        if commit:
            bet.save()
        return bet
