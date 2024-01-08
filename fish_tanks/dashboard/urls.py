from django.urls import path, include

from .views import *

app_name = 'fish_tanks'

urlpatterns = [
    path('htmx/', include('fish_tanks.dashboard.htmx.urls', namespace='htmx')),
    path('all/', FishTankListView.as_view(), name='fish_tank_list'),
    path('create/', FishTankCreateView.as_view(), name='fish_tank_create'),
    path('detail/<int:pk>/', FishTankDetailView.as_view(), name='fish_tank_detail'),
    path('detail/<int:pk>/update/', FishTankUpdateView.as_view(), name='fish_tank_update'),
]
