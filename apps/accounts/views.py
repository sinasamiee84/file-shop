# apps/accounts/views.py

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from apps.accounts.forms import LoginForm, RegisterForm
from apps.accounts.models import CustomUser


class Login(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm
    next_page = reverse_lazy("home")


class Logout(LogoutView):
    next_page = reverse_lazy("accounts:login")


class Register(CreateView):
    model = CustomUser
    form_class = RegisterForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, "ثبت‌نام با موفقیت انجام شد. خوش آمدی!")
        return response
