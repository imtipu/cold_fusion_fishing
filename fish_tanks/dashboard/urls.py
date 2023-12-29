from django.urls import path, include

from .views import *

app_name = 'fish_tanks'

urlpatterns = [
    path('htmx/', include('fish_tanks.dashboard.htmx.urls', namespace='htmx')),
    path('all/', FishTankListView.as_view(), name='fish_tank_list'),
    path('create/', FishTankCreateView.as_view(), name='fish_tank_create'),
    path('deatil/<int:pk>/', FishTankDetailView.as_view(), name='fish_tank_detail'),
]
