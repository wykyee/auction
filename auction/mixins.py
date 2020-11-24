from django.contrib.auth.mixins import AccessMixin

from auction.services import get_post_by_pk


class AuthorRequiredMixin(AccessMixin):
	def dispatch(self, request, *args, **kwargs):
		"""
		User must either superuser or author of certain post.
		"""
		user = request.user
		post = get_post_by_pk(kwargs.get("pk"))

		if post:
			if all([not user.is_superuser, user != post.author]):
				return self.handle_no_permission()
		return super().dispatch(request, *args, **kwargs)
