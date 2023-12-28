from django.urls import path, include

app_name = 'v1'

urlpatterns = [
    path('accounts/', include('users.accounts.api.v1.urls', namespace='accounts')),
    path('fish-tanks/', include('fish_tanks.api.v1.urls', namespace='fish_tanks')),
]
