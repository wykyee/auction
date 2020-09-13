from django import forms

from auction.models import Bet


class BetForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        """
        Gets author for initial parameter to save it as author of post.
        """
        self.better = kwargs.pop('better', None)
        self.post = kwargs.pop('post', None)
        super(BetForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Bet
        fields = ["amount", ]

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
