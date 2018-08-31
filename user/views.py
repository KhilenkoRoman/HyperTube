from django.shortcuts import render, redirect
from index.models import User
from allauth.socialaccount.models import SocialAccount


def user_profile(request, provider=None):
	user = request.user
	if user.id is None:
		return redirect('index')

	print(provider)

	accounts = SocialAccount.objects.filter(user=user)
	active_providers = []
	for account in accounts.values():
		active_providers.append(account['provider'])

	context = {'profile_user': user,
	           'active_providers': active_providers,
	           }
	return render(request, 'user/user.html', context)


def social_activated(request, provider):
	return redirect('user_profile')

