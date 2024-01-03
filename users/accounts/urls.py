from django.urls import path
from .views import *

urlpatterns = [
    path('logout/', AccountLogoutView.as_view(), name='account_logout'),
    path('profile/', AccountProfileView.as_view(), name='account_profile'),
    path('password/change/', AccountPasswordChangeView.as_view(), name='account_password_change'),
]
