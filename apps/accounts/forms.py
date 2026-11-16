from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm as DjangoAuthenticationForm,
    UserCreationForm as DjangoUserCreationForm,
)

User = get_user_model()


class RegisterForm(DjangoUserCreationForm):
    email = forms.EmailField(
        label="ایمیل",
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "ایمیل"}),
    )

    class Meta(DjangoUserCreationForm.Meta):
        model = User
        fields = ("username", "email")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("این ایمیل قبلاً ثبت شده است.")
        return email


class LoginForm(DjangoAuthenticationForm):
    username = forms.CharField(
        label="نام کاربری",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "نام کاربری"}),
    )
    password = forms.CharField(
        label="رمز عبور",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "رمز عبور"}),
    )
