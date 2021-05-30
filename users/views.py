from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import views

from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy("login")
    template_name = "users/signup.html"


class LoginView(views.LoginView):
    template_name = 'users/registration/login.html'


class LogoutView(views.LogoutView):
    template_name = 'users/registration/logged_out.html'


class PasswordResetDoneView(views.PasswordResetDoneView):
    template_name = 'users/registration/password_reset_done.html'


class PasswordResetConfirmView(views.PasswordResetConfirmView):
    template_name = 'users/registration/password_reset_confirm.html'


class PasswordResetCompleteView(views.PasswordResetCompleteView):
    template_name = 'users/registration/password_reset_complete.html'


class PasswordChangeView(views.PasswordChangeView):
    template_name = 'users/registration/password_change_form.html'


class PasswordChangeDoneView(views.PasswordChangeDoneView):
    template_name = 'users/registration/password_change_done.html'
