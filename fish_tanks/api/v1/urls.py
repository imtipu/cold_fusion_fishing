from django.urls import path

from . import views

app_name = 'fish_tanks'

urlpatterns = [
    path('all/', views.FishTankListAPIView.as_view(), name='list'),
    path('detail/<int:pk>/', views.FishTankDetailAPIView.as_view(), name='detail'),
    path('dropdown-list/', views.FishTankDropDownlistAPIView.as_view(), name='dropdown_list'),
]
