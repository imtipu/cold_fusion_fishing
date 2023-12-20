from django.urls import path, include
from .views import *

app_name = 'dashboard'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('htmx/', include('dashboard.htmx.urls', namespace='htmx')),
    path('fish-tanks/', include('fish_tanks.dashboard.urls', namespace='fish_tanks')),
    path('projects/', include('projects.dashboard.urls', namespace='projects')),
]
