import datetime

from django import forms
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from auction.models import Bet, Post


class DateInputCalendar(forms.DateInput):
	input_type = "datetime-local"


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


class PostForm(forms.ModelForm):
	TODAY = timezone.localtime(timezone.now()).strftime('%d\%m\%Y, %H:%M')

	title = forms.CharField(
		widget=forms.TextInput(attrs={"class": "form-control"}),
		label=_("Название"),
	)
	main_image = forms.FileField(
		required=False,
		widget=forms.FileInput(attrs={"class": "custom-file-input"}),
		label=_("Отображаемая картинка")
	)
	description = forms.CharField(
		required=False, widget=forms.Textarea(attrs={"class": "form-control"}),
		label=_("Описание"),
	)
	available_till = forms.DateTimeField(
		required=True, widget=DateInputCalendar(
			attrs={"class": "form-control", "min": f"{TODAY}"}
		), label=_("Пост доступен до"),
	)

	class Meta:
		model = Post
		fields = ("title", "permanent_price",
		          "initial_bet", "description", "main_image",
		          "available_till")
		widgets = {
			"permanent_price": forms.NumberInput(
				attrs={"class": "form-control"}),
			"initial_bet": forms.NumberInput(attrs={"class": "form-control"}),
		}

	def __init__(self, *args, **kwargs):
		self.author = kwargs.pop("author")
		super().__init__(*args, **kwargs)

	def save(self, commit=True):
		"""
		Saves user from request as author of created post.
		"""
		post = super().save(commit=False)
		post.author = self.author
		if commit:
			post.save()
		return post

	def clean(self):
		"""
		Validates data in permanent_price and initial_bet
		"""
		cleaned_data = super().clean()
		initial_bet = cleaned_data["initial_bet"]
		permanent_price = cleaned_data["permanent_price"]
		available_till = cleaned_data["available_till"]

		if initial_bet == 0:
			self.add_error("initial_bet",
			               _("Начальная ставка не может быть < 0"))

		if permanent_price == 0:
			self.add_error("permanent_price",
			               _("Цена выкупа не может быть < 0"))

		if permanent_price <= initial_bet:
			self.add_error("permanent_price",
			               _("Цена выкупа не может быть меньше ставки"))

		if available_till <= timezone.localtime(timezone.now()):
			self.add_error("available_till",
			               _("Дата невалидна"))

		return cleaned_data


class PostCreateForm(PostForm):
	pass


class PostUpdateForm(PostForm):
	class Meta:
		model = Post
		fields = ("title", "permanent_price", "description", "main_image")
		widgets = {
			"permanent_price": forms.NumberInput(
				attrs={"class": "form-control"}),
		}

	def clean(self):
		"""
		Validates data in permanent_price and current bet
		"""
		cleaned_data = super(PostForm, self).clean()
		permanent_price = cleaned_data["permanent_price"]
		try:
			bet = self.instance.last_bet.amount
		except AttributeError:
			bet = self.instance.initial_bet

		if permanent_price == 0:
			self.add_error("permanent_price",
			               _("Цена выкупа не может быть < 0"))

		if permanent_price <= bet:
			self.add_error(
				"permanent_price",
				_("Цена выкупа не может быть меньше действующей ставки"))

		return cleaned_data


class PostSortForm(forms.Form):
	PRICE_CHOICES = (
		("", "------------"),
		("from_cheapest", _("От дешевых к дорогим")),
		("from_expensive", _("От дорогих к дешевым")),
	)
	CREATED_CHOICES = (
		("", "------------"),
		("from_newest", _("От новых к старым")),
		("from_oldest", _("От старых к новым")),
	)

	price = forms.ChoiceField(
		choices=PRICE_CHOICES, required=False,
		label=_("Цена"), widget=forms.Select(attrs={"class": "form-control"})
	)
	created = forms.ChoiceField(
		choices=CREATED_CHOICES, required=False,
		label=_("Создано"),
		widget=forms.Select(attrs={"class": "form-control"})
	)
	author = forms.CharField(
		widget=forms.TextInput(
			attrs={"class": "form-control", "placeholder": _("Имя автора")}
		), required=False, label=_("Автор")
	)
	post_title = forms.CharField(
		widget=forms.TextInput(
			attrs={"class": "form-control", "placeholder": _("Название лота")}
		), required=False, label=_("Название лота")
	)
