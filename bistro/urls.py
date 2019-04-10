from django.urls import path

from . import views

app_name = 'bistro'

urlpatterns = [
    path('random_bistro/', views.random_bistro, name='random_bistro'),
    path('add_place/', views.add_place, name='add_place'),
]
