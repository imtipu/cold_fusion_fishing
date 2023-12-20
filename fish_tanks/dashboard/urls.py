from django.urls import path, include

from .views import *

app_name = 'fish_tanks'

urlpatterns = [
    path('htmx/', include('fish_tanks.dashboard.htmx.urls', namespace='htmx')),
    path('', FishTankListView.as_view(), name='fish_tank_list'),
    path('<int:pk>/', FishTankDetailView.as_view(), name='fish_tank_detail'),
]
