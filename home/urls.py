from django.urls import path
from django.views.i18n import set_language

from .views import *

app_name = 'home'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    # path('change-language/', ChangeLanguageView.as_view(), name='set_language'),
    path('set-language/', set_language, name='set_language'),
]
