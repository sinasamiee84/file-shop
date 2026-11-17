# apps/accounts/views.py

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from apps.accounts.forms import LoginForm, RegisterForm , CustomPasswordChangeForm
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



class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = "accounts/change_password.html"
    success_url = reverse_lazy("home")  # یا نام صفحه دلخواه مثل محصولات

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "رمز عبور شما با موفقیت تغییر کرد.")
        return response
