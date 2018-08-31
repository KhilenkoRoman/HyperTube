from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
	def get_connect_redirect_url(self, request, socialaccount):
		path = "/user/social_activated/{provider}"
		# return path.format(username=request.user.username)
		return path.format(provider=socialaccount.provider)


# class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
# 	def save_user(self, request, sociallogin, form):
# 		user = super(CustomSocialAccountAdapter, self).save_user(request, sociallogin, form)
# 		# Do what ever you want with the user
# 		return user