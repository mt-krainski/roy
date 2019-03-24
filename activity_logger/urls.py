from django.urls import path
from . import views

app_name = 'activity_logger'
urlpatterns = [
    path('activity_manager/', views.activity_manager, name='activity_manager'),
]
