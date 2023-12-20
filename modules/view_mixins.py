from django.contrib.auth.mixins import LoginRequiredMixin


class AdminLoginRequiredMixin(LoginRequiredMixin):
    # login_url = '/accounts/login/'
    pass
