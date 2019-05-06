from django.urls import path

from . import views

app_name = 'notes'
urlpatterns = [
    path('note/', views.note_view, name='note-view'),
]
