from django.shortcuts import render
from django.conf import settings


def search(request):
    context = {'APP_PATH': settings.APP_PATH}
    return render(request, 'search/search.html', context)
