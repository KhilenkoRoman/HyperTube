from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


def index(request):
	context = {'APP_PATH': settings.APP_PATH}
	return render(request, 'index/index.html', context)


# render_to_response('index/index.html', {}, context_instance=RequestContext(request))


def ajax_login(request):
	if request.method != 'POST':
		return redirect('index')
	user = authenticate(username=request.POST.get('login'), password=request.POST.get('password'))
	print(user)
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

	print(request.POST)
	if request.POST.get('pwd1') != request.POST.get('pwd1'):
		return HttpResponse("error pwd")

	if User.objects.filter(email=request.POST.get('email')):
		return HttpResponse("email exist")
	if User.objects.filter(username=request.POST.get('login')):
		return HttpResponse("login exist")

	try:
		user = User.objects.create_user(request.POST.get('login'), request.POST.get('email'), request.POST.get('pwd1'))
	except:
		return HttpResponse("error")

	user.first_name = request.POST.get('first_name')
	user.last_name = request.POST.get('last_name')

	return HttpResponse("sucsess")
