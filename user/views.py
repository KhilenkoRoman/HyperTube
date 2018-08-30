from django.shortcuts import render, redirect
from index.models import User


def user_profile(request):
	user = request.user
	if user.id is None:
		print('asdasd')
		return redirect('index')

	print(user.id)

	context = {'profile_user': user,
	           'qwe': "asd",
	           }
	return render(request, 'user/user.html', context)
