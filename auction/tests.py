from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

from auction.forms import PostForm
from auction.models import Post


class ModelTest(TestCase):
	@classmethod
	def setUpTestData(cls):
		get_user_model().objects.create(
			**{'username': 'testuser', 'password': '123'})
		profile = get_user_model().objects.get(username='testuser')
		post_data = {
			'title': "TestTitle",
			'permanent_price': 1000,
			'initial_bet': 20,
			'author': profile
		}
		Post.objects.create(**post_data)

	def test_absolute_url(self):
		post = Post.objects.get(id=1)
		self.assertEquals(post.get_absolute_url(), '/post/1/')

	def test_get_update_url(self):
		post = Post.objects.get(id=1)
		self.assertEquals(post.get_update_url(), '/post/1/update/')

	def test_get_delete_url(self):
		post = Post.objects.get(id=1)
		self.assertEquals(post.get_delete_url(), '/post/1/delete/')


class PostFormTest(TestCase):
	@classmethod
	def setUpTestData(cls):
		get_user_model().objects.create(**{'username': "test",
		                                   'password': "123"})

	def test_initial_bet_zero(self):
		form_data = {
			'title': "SomeTitle",
			'permanent_price': 1000,
			'initial_bet': 0,
			'available_till': timezone.localtime(
				timezone.now()
			) + timezone.timedelta(days=1)
		}
		form = PostForm(data=form_data,
		                author=get_user_model().objects.get(id=1))
		self.assertFalse(form.is_valid())

	def test_permanent_price_zero(self):
		form_data = {
			'title': "SomeTitle",
			'permanent_price': 0,
			'initial_bet': 1000,
			'available_till': timezone.localtime(
				timezone.now()
			) + timezone.timedelta(days=1)
		}
		form = PostForm(data=form_data,
		                author=get_user_model().objects.get(id=1))
		self.assertFalse(form.is_valid())

	def test_permanent_less_initial(self):
		form_data = {
			'title': "SomeTitle",
			'permanent_price': 100,
			'initial_bet': 101,
			'available_till': timezone.localtime(
				timezone.now()
			) + timezone.timedelta(days=1)
		}
		form = PostForm(data=form_data,
		                author=get_user_model().objects.get(id=1))
		self.assertFalse(form.is_valid())

	def test_available_till_less_now(self):
		form_data = {
			'title': "SomeTitle",
			'permanent_price': 100,
			'initial_bet': 99,
			'available_till': timezone.localtime(
				timezone.now()
			) - timezone.timedelta(days=1)
		}
		form = PostForm(data=form_data,
		                author=get_user_model().objects.get(id=1))
		self.assertFalse(form.is_valid())
