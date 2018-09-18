from django.shortcuts import render, redirect
from allauth.socialaccount.models import SocialAccount
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import update_session_auth_hash
from a_index.views import html_escape
from django.core.files.images import get_image_dimensions
import re
import os
from django.conf import settings


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
	print(user.avatar)

	return render(request, 'user/user.html', context)


def social_activated(request, provider):
	request.session['last_social_connect'] = provider
	return redirect('user_profile')


def ajax_user_change_pwd(request):
	if request.method != 'POST':
		return HttpResponse("error")
	current_user = request.user
	if not current_user:
		return HttpResponse("error")

	pwd1 = request.POST.get('pwd1')
	pwd2 = request.POST.get('pwd2')

	if len(pwd1) < 4 or len(pwd1) > 100 or pwd1 != pwd2:
		return HttpResponse("error")

	current_user.set_password(request.POST['pwd1'])
	current_user.save()
	update_session_auth_hash(request, current_user)

	return HttpResponse("sucsess")


def ajax_user_change_info(request):
	errors = []
	if request.method != 'POST':
		return HttpResponse("error")
	current_user = request.user
	if not current_user:
		return HttpResponse("error")

	email = html_escape(request.POST.get('email'))
	first_name = html_escape(request.POST.get('first_name'))
	last_name = html_escape(request.POST.get('last_name'))

	if not email or len(email) > 100:
		errors.append("error_email")
	elif not re.match("^[a-z0-9-]+(.[_a-z0-9-]+)*@[a-z0-9-]+(.[a-z0-9-]+)*(.[a-z]{2,4})$", email):
		errors.append("error_email")
	elif current_user.email != email and User.objects.filter(email=email):
		errors.append("error_email")
	else:
		current_user.email = email

	if not first_name or len(first_name) > 100:
		errors.append("error_first_name")
	else:
		current_user.first_name = first_name

	if not last_name or len(last_name) > 100:
		errors.append("error_last_name")
	else:
		current_user.last_name = last_name

	if len(errors) == 0:
		current_user.save()
		errors.append("success")
	return JsonResponse(list(set(errors)), safe=False)


def ajax_change_avatar(request):
	if request.method != 'POST':
		return HttpResponse("error")
	current_user = request.user
	if not current_user:
		return HttpResponse("error")

	avatar = request.FILES.get('avatar')
	if not avatar:
		return HttpResponse("error")

	print(type(avatar))
	try:
		w, h = get_image_dimensions(avatar)
		if w > 1000 or h > 1000:
			return HttpResponse("img_size_error")
		main, sub = avatar.content_type.split('/')
		if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
			return HttpResponse("img_format_error")
	except:
		return HttpResponse("error")

	path = settings.MEDIA_ROOT + "/" + current_user.avatar.name
	if os.path.isfile(path):
		os.remove(path)
	current_user.avatar = avatar
	current_user.save()
	return HttpResponse(current_user.avatar.url)
