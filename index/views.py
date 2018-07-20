from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.conf import settings


def index(request):
    context = {'APP_PATH': settings.APP_PATH}
    return render(request, 'index/index.html', context)
    # render_to_response('index/index.html', {}, context_instance=RequestContext(request))
