from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('home-project-list/', views.HomePageProjectListAPIView.as_view(), name='home_project_list'),
    path('all/', views.ProjectListAPIView.as_view(), name='project_list'),
    path('detail/<int:pk>/', views.ProjectDetailAPIView.as_view(), name='project_detail'),
    path('detail/<int:pk>/daily-activities/', views.ProjectDailyActivityListAPIView.as_view(),
         name='project_daily_activity_list'),
]
