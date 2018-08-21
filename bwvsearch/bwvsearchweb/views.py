from django.shortcuts import render
from django.http import HttpResponse

from .models import Score

def index(request):
    return render(request, 'bwvsearchweb/index.html')

def search(request):
    chords = request.POST['chords']
    hits = Score.objects.with_pitched_chords(chords)
    return render(request, 'bwvsearchweb/search.html', {
        'chords': chords,
        'hits': hits
    })
    