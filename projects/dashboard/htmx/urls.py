from django.urls import path

from . import views

app_name = 'htmx'

urlpatterns = [
     path('detail/<int:pk>/daily-activities/', views.HtmxDailyActivityTableListView.as_view(),
         name='htmx_daily_activity_table_list'),
     path('detail/<int:pk>/add-daily-activity-form/', views.htmx_daily_activity_activity_form,
         name='htmx_add_daily_activity_form'),
     # path('add-daily-activity-form/', views.htmx_daily_activity_activity_form,
     #     name='htmx_add_daily_activity_form'),

]
