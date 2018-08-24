from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth import authenticate, login
from index.models import User
from django.http import JsonResponse
import re
import random
from hashlib import md5
from django.utils import timezone
from django.core.mail import send_mail
from datetime import datetime
from datetime import timedelta


def html_escape(text):
	html_escape_table = {
		"&": "&amp;",
		'"': "&quot;",
		"'": "&apos;",
		">": "&gt;",
		"<": "&lt;",
	}
	return "".join(html_escape_table.get(c, c) for c in text)


def index(request):
	context = {'APP_PATH': settings.APP_PATH}
	return render(request, 'index/index.html', context)


def user_profile(request, get_login):
	user = User.objects.filter(username=get_login)
	if len(user) == 1:
		user = user[0]
	else:
		user = None
	context = {'profile_user': user,
	           'qwe': "asd",
	           }
	return render(request, 'index/user.html', context)


def activation(request):
	if request.user.is_authenticated:
		return redirect('index')

	activation_key = request.GET.get('activation_key')
	a_login = request.GET.get('user')

	user = User.objects.get(username=a_login)
	print(user.activation_key)
	print(activation_key)
	a_response = "111"
	if not user:
		a_response = "No such user"
	elif user.is_active:
		a_response = "User is active"
	elif user.activation_key == activation_key:
		if user.activation_key_time + timedelta(days=1) < timezone.now():
			a_response = "Key is outdated"
		else:
			user.is_active = True
			user.save()
			login(request, user, 'django.contrib.auth.backends.ModelBackend')
			a_response = "User activated"

	# print(timezone.now())
	# print(user.activation_key_time + timedelta(days=2))
	# print(user.activation_key_time + timedelta(days=2) < timezone.now())



	context = {'response': a_response}
	return render(request, 'index/activation.html', context)

# render_to_response('index/index.html', {}, context_instance=RequestContext(request))


def ajax_login(request):
	if request.method != 'POST':
		return redirect('index')
	user = authenticate(username=request.POST.get('login'), password=request.POST.get('password'))
	if user is not None:
		login(request, user)
		return HttpResponse("sucses")
	else:
		return HttpResponse("error")


def ajax_reset(request):
	if request.method != 'POST':
		return redirect('index')
	user = User.objects.filter(email=request.POST.get('email'))
	if user:
		return HttpResponse("sucsess")
	else:
		return HttpResponse("error")


def ajax_register(request):
	if request.method != 'POST':
		return redirect('index')

	email = html_escape(request.POST.get('email'))
	rlogin = html_escape(request.POST.get('login'))
	first_name = html_escape(request.POST.get('first_name'))
	last_name = html_escape(request.POST.get('last_name'))

	errors = []
	if not rlogin or len(rlogin) > 100:
		errors.append("error_login")
	if not re.match("^[a-zA-Z0-9.+\-_]+$", rlogin):
		errors.append("error_login")
	if User.objects.filter(username=rlogin):
		errors.append("error_login")

	if not email or len(email) > 100:
		errors.append("error_email")
	if not re.match("^[a-z0-9-]+(.[_a-z0-9-]+)*@[a-z0-9-]+(.[a-z0-9-]+)*(.[a-z]{2,4})$", email):
		errors.append("error_email")
	if User.objects.filter(email=email):
		errors.append("error_email")

	if not request.POST.get('pwd1') or len(request.POST.get('pwd1')) > 100 or len(request.POST.get('pwd1')) < 4:
		errors.append("error_pwd")
	if request.POST.get('pwd1') != request.POST.get('pwd2'):
		errors.append("error_pwd")

	if not first_name or len(first_name) > 100:
		errors.append("error_first_name")
	if not last_name or len(last_name) > 100:
		errors.append("error_last_name")

	if len(errors) == 0:
		try:
			user = User.objects.create_user(rlogin, email, request.POST.get('pwd1'))
			user.first_name = first_name
			user.last_name = last_name
			activation_key = md5((rlogin + str(random.randrange(1000))).encode('utf-8')).hexdigest()
			user.activation_key = activation_key
			user.activation_key_time = timezone.now()
			user.is_active = False
			user.save()
			return_email = re.search(r'(@[a-z0-9-]+(.[a-z0-9-]+)*(.[a-z]{2,4})$)', email).group(0)
			activation_link = "https://localhost:8000/activation?user=" + rlogin + "&activation_key=" + activation_key
			html_message = """
			        <p>Hi %s %s</p>
			        <p>To complete registration follow the link</p>
			        <a href="%s">Link</p>
			        """ % (first_name, last_name, activation_link)

			send_mail('HyperTube registration', "", 'rkhilenksmtp@gmail.com',
			          [email, ], html_message=html_message, fail_silently=True)

			return JsonResponse(["success", "https://" + return_email[1:]], safe=False)
		except:
			errors.append("error_creation")

	return JsonResponse(list(set(errors)), safe=False)
