from django.shortcuts import render
from index.models import User


def user_profile(request, get_login):
	user = User.objects.filter(username=get_login)
	if len(user) == 1:
		user = user[0]
	else:
		user = None
	context = {'profile_user': user,
	           'qwe': "asd",
	           }
	return render(request, 'user/user.html', context)
