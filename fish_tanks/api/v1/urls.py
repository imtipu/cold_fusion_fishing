from django.urls import path

from . import views

app_name = 'fish_tanks'

urlpatterns = [
    path('all/', views.FishTankListAPIView.as_view(), name='list'),
    path('dropdown-list/', views.FishTankDropDownlistAPIView.as_view(), name='list'),
]
