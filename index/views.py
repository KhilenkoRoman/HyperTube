from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    context = {}
    return render(request, 'index/index.html', context)
    # return HttpResponse("This is Spa** khm Hypertube")
