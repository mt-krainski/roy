from django.urls import path

from . import views

app_name = 'activity_logger'
urlpatterns = [
    path('activity_manager/', views.activity_manager_view, name='activity_manager'),
    path('summary/', views.summary_view, name='summary-view')
]
