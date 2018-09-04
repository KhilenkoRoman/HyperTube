from django.shortcuts import render, redirect
from index.models import User
from allauth.socialaccount.models import SocialAccount


def user_profile(request):
	user = request.user
	if user.id is None:
		return redirect('index')

	accounts = SocialAccount.objects.filter(user=user)
	active_providers = []
	for account in accounts.values():
		active_providers.append(account['provider'])

	last_social_connect = request.session.get('last_social_connect', None)
	request.session['last_social_connect'] = None

	context = {'profile_user': user,
	           'active_providers': active_providers,
	           'last_social_connect': last_social_connect,
	           }
	return render(request, 'user/user.html', context)


def social_activated(request, provider):
	request.session['last_social_connect'] = provider
	return redirect('user_profile')

