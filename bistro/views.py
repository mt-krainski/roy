from random import randint

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.text import slugify

from bistro.forms import PlaceForm
from .models import BistroPlace


@login_required
def random_bistro(request):
    place_qs = BistroPlace.objects.filter(user=request.user)
    if place_qs.exists():
        random_id = randint(0, place_qs.count()-1)
        context = {
            'bistro': place_qs[random_id],
        }
    else:
        context = {
            'bistro': None,
        }
    return render(
        request, 'bistro/bistro.html', context)


@login_required
def add_place(request):
    if request.method == 'POST':

        form = PlaceForm(request.POST)

        if form.is_valid():
            new_place = BistroPlace(
                name=form.cleaned_data['place_name'],
                slug=slugify(form.cleaned_data['place_name']),
                location=form.cleaned_data['location'],
                user=request.user,
                type=form.cleaned_data['type'],
            )
            new_place.save()

            messages.add_message(
                request,
                messages.INFO,
                f'{new_place.name.capitalize()} has been added!')

            return HttpResponseRedirect(
                reverse('bistro:add_place'))

        return HttpResponseBadRequest

    else:
        form = PlaceForm()
    return render(request, 'bistro/add.html', {'form': form})
