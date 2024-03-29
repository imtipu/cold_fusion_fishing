from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('home-project-list/', views.HomePageProjectListAPIView.as_view(), name='home_project_list'),
    path('all/', views.ProjectListAPIView.as_view(), name='project_list'),
]