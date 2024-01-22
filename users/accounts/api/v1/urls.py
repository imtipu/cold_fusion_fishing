from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/token/', views.TokenLoginAPIView.as_view(), name='token_login'),
    path('profile/', views.AccountProfileAPIView.as_view(), name='profile'),
]
