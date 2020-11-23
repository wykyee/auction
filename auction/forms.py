from django import forms
from django.utils.translation import ugettext_lazy as _

from auction.models import Bet, Post


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
            "amount": _("Ставка"),
        }

    def clean_amount(self) -> int:
        """
        Checks if input amount is in limits.
        """
        data = self.cleaned_data["amount"]

        if self.current_bet >= data or data >= self.post.permanent_price:
            self.add_error("amount", _("Ваша ставка невалидна"))

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


class PostCreateForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    main_image = forms.FileField(
        required=False, widget=forms.FileInput(attrs={"class": "form-control"})
    )
    description = forms.CharField(
        required=False, widget=forms.Textarea(attrs={"class": "form-control"})
    )

    class Meta:
        model = Post
        fields = ("title", "permanent_price",
                  "initial_bet", "description", "main_image")
        widgets = {
            "permanent_price": forms.NumberInput(attrs={"class": "form-control"}),
            "initial_bet": forms.NumberInput(attrs={"class": "form-control"}),
        }
        
    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop("author")
        super(PostCreateForm, self).__init__(*args, **kwargs)
        
    def save(self, commit=True):
        """
        Saves user from request as author of created post.
        """
        post = super(PostCreateForm, self).save(commit=False)
        post.author = self.author
        if commit:
            post.save()    
        return post
    
    def clean(self):
        """
        Validates data in permanent_price and initial_bet
        """
        cleaned_data = super(PostCreateForm, self).clean()
        initial_bet = cleaned_data["initial_bet"]
        permanent_price = cleaned_data["permanent_price"]

        if initial_bet == 0:
            self.add_error("initial_bet",
                           _("Начальная ставка не может быть < 0"))

        if permanent_price == 0:
            self.add_error("permanent_price", _("Цена выкупа не может быть < 0"))

        if permanent_price <= initial_bet:
            self.add_error("permanent_price",
                           _("Цена выкупа не может быть меньше ставки"))

        return cleaned_data


class PostSortForm(forms.Form):
    PRICE_CHOICES = (
        ("from_cheapest", _("От дешевых к дорогим")),
        ("from_expensive", _("От дорогих к дешевым")),
    )
    CREATED_CHOICES = (
        ("newest", _("От новых к старым")),
        ("oldest", _("От старых к новым")),
    )

    price = forms.ChoiceField(choices=PRICE_CHOICES,
                              required=False, label=_("Цена"))
    created = forms.ChoiceField(choices=CREATED_CHOICES,
                                required=False, label=_("Создано"))
    author = forms.CharField(widget=forms.TextInput(),
                             required=False, label=_("Автор"))
