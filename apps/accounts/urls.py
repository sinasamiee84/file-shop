from django.urls import path

from .views import Login , Logout,Register , CustomPasswordChangeView

app_name = "accounts"

urlpatterns = [
    path("login/", Login.as_view(), name="login"),
    path("logout/", Logout.as_view(), name="logout"),
    path("register/", Register.as_view(), name="register"),
    path("change-pasword/", CustomPasswordChangeView.as_view(), name="change_password"),
]