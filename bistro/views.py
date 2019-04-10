from random import randint

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Place


@login_required
def random_bistro(request):
    place_qs = Place.objects.filter(user=request.user)
    if place_qs.exists():
        random_id = randint(0, place_qs.count()-1)
        context = {
            'bistro': place_qs[random_id],
        }
    else:
        context = {
            'bistro': 'You didn\'t add any places yet!',
        }
    return render(
        request, 'bistro/bistro.html', context)
