from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import authenticate, login
from a_user.models import CustomUserModel
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
    if not request.session.get("lang"):
        request.session["lang"] = 1
    if request.user.id:
        return redirect('user_profile')
    context = {'APP_PATH': settings.APP_PATH}
    return render(request, 'index/index.html', context)


def activation(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.GET.get('activation_key') and request.GET.get('a_user'):
        activation_key = request.GET.get('activation_key')
        a_login = request.GET.get('a_user')
    else:
        context = {'response': "error"}
        return render(request, 'index/activation.html', context)

    user = CustomUserModel.objects.get(username=a_login)
    print(user.activation_key)
    print(activation_key)
    a_response = "111"
    if not user:
        a_response = "No such a_user"
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

    context = {'response': a_response}
    return render(request, 'index/activation.html', context)


def reset_pwd(request):
    if request.user.is_authenticated:
        return redirect('index')

    rc_key = request.GET.get('recovery_key')
    rc_login = request.GET.get('a_user')

    try:
        user = CustomUserModel.objects.get(username=rc_login)
    except:
        context = {'response': "No such a_user"}
        return render(request, 'index/reset_pwd.html', context)
    a_response = "error"
    if not user:
        a_response = "No such a_user"
    elif user.recovery_key != rc_key or user.recovery_key == "":
        a_response = "wrong key"
    else:
        if user.recovery_key_time + timedelta(days=1) < timezone.now():
            a_response = "Key is outdated"
        else:
            a_response = "sucsess"
    context = {'response': a_response, 'username': rc_login, 'key': rc_key}
    return render(request, 'index/reset_pwd.html', context)


def ajax_login(request):
    if request.method != 'POST':
        return redirect('index')

    lgn = request.POST.get('login')
    paswd = request.POST.get('password')

    user = authenticate(username=lgn, password=paswd)

    errors = []
    if not lgn:
        errors.append("error_login")
    if not paswd:
        errors.append("error_password")
    if len(errors) == 0:
        try:
            login(request, user)
            return JsonResponse(["success"], safe=False)
        except:
            errors.append("error_log_in")
    return JsonResponse(list(set(errors)), safe=False)


def ajax_new_pwd(request):
    if request.method != 'POST':
        return redirect('index')

    if len(request.POST.get('pwd1')) < 4 or len(request.POST.get('pwd1')) > 100 or request.POST.get(
            'pwd1') != request.POST.get('pwd2'):
        return HttpResponse("error")
    try:
        user = CustomUserModel.objects.get(username=request.POST['username'])
    except:
        return HttpResponse("error")
    if user.recovery_key == "":
        return HttpResponse("error")
    if user.recovery_key == request.POST['key']:
        if user.recovery_key_time + timedelta(days=1) < timezone.now():
            return HttpResponse("error")
        else:
            user.set_password(request.POST['pwd1'])
            user.recovery_key = ""
            user.save()
            return HttpResponse("sucsess")


def ajax_reset(request):
    if request.method != 'POST':
        return redirect('index')
    try:
        user = CustomUserModel.objects.get(email=request.POST.get('email'), is_active=True)
    except:
        return HttpResponse("error")
    if user:
        user.recovery_key = md5((user.username + str(random.randrange(1234))).encode('utf-8')).hexdigest()
        user.recovery_key_time = timezone.now()
        user.save()
        return_email = re.search(r'(@[a-z0-9-]+(.[a-z0-9-]+)*(.[a-z]{2,4})$)', user.email).group(0)

        recovery_link = "https://localhost:8000/reset_pwd?a_user=" + user.username + "&recovery_key=" + user.recovery_key
        html_message = """
					        <p>Hi %s %s</p>
					        <p>To reset password follow the link</p>
					        <a href="%s">Link</p>
					        """ % (user.first_name, user.last_name, recovery_link)

        send_mail('HyperTube pasword reset', "", 'rkhilenksmtp@gmail.com',
                  [user.email, ], html_message=html_message, fail_silently=True)

        return HttpResponse("https://" + return_email[1:])
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
    if CustomUserModel.objects.filter(username=rlogin):
        errors.append("error_login")

    if not email or len(email) > 100:
        errors.append("error_email")
    if not re.match("^[a-z0-9-]+(.[_a-z0-9-]+)*@[a-z0-9-]+(.[a-z0-9-]+)*(.[a-z]{2,4})$", email):
        errors.append("error_email")
    if CustomUserModel.objects.filter(email=email):
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
            user = CustomUserModel.objects.create_user(rlogin, email, request.POST.get('pwd1'))
            user.first_name = first_name
            user.last_name = last_name
            activation_key = md5((rlogin + str(random.randrange(1000))).encode('utf-8')).hexdigest()
            user.activation_key = activation_key
            user.activation_key_time = timezone.now()
            user.is_active = False
            user.save()
            return_email = re.search(r'(@[a-z0-9-]+(.[a-z0-9-]+)*(.[a-z]{2,4})$)', email).group(0)
            activation_link = "https://localhost:8000/activation?a_user=" + rlogin + "&activation_key=" + activation_key
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


def change_lang(request, lang):
    if lang == 'en':
        request.session["lang"] = 1
    elif lang == 'ru':
        request.session["lang"] = 2

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
