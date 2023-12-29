from django.urls import path, include

from .views import *

app_name = 'projects'

urlpatterns = [
    path('all/', ProjectListView.as_view(), name='project_list'),
    path('create/', ProjectCreateView.as_view(), name='project_create'),
    path('htmx/', include('projects.dashboard.htmx.urls')),
    path('detail/<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('detail/<int:pk>/daily-activities/', ProjectDailyActivityListView.as_view(), name='project_daily_activity_list'),
    path('detail/<int:pk>/add-activity/', DailyActivityAddView.as_view(), name='add_project_activity'),
    path('daily-activities/<int:pk>/', ProjectDailyActivityDetailView.as_view(), name='project_activity_detail'),
]
