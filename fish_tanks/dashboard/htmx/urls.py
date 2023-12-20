from django.urls import path

from .views import *

app_name = 'htmx'

urlpatterns = [
    path('fish-tank-list/', HtmxFistTankListView.as_view(), name='fish_tank_list'),
    path('detail/<int:pk>/quick-view/', FishTankQuickView.as_view(), name='fish_tank_quick_view'),

]
