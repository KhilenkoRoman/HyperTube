from django.shortcuts import render


def player(request):
    context = {}
    return render(request, 'player/player.html', context)
