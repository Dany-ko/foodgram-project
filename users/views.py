from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import views
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404


from users.forms import CreationForm, PasswordResetForm
from recipes.models import User


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy("login")
    template_name = "users/signup.html"

    def form_valid(self, form):
        data = form.data
        subject = 'Добро пожаловать на Foodgram. Регистрация прошла успешно'
        content = f'''
            {data["first_name"]}, спасибо за регистрацию на Foodgram.
            Ваш email - {data["email"]}
            Ваш логин - {data["username"]}
            Ваш пароль - {self.request.POST.get('password1')}
        '''
        send_mail(
            subject,
            content,
            settings.EMAIL_HOST_USER,
            [f'{data["email"]}']
        )
        return super().form_valid(form)


class LoginView(views.LoginView):
    template_name = 'users/registration/login.html'


class LogoutView(views.LogoutView):
    template_name = 'users/registration/logged_out.html'


class PasswordResetDoneView(views.PasswordResetDoneView):
    template_name = 'users/registration/password_reset_done.html'


class PasswordResetView(views.PasswordResetView):
    form_class = PasswordResetForm
    template_name = 'users/registration/password_reset_form.html'


class PasswordResetCompleteView(views.PasswordResetCompleteView):
    template_name = 'users/registration/password_reset_complete.html'


class PasswordChangeView(views.PasswordChangeView):
    template_name = 'users/registration/password_change_form.html'

    def form_valid(self, form):
        data = form.data
        user = get_object_or_404(
            User,
            username=self.request.user.username
        )
        subject = 'Ваш пароль был изменен.'
        content = f'''
            {user.username}, Ваш пароль был изменен на новый.
            Ваш email - {user.email}
            Ваш логин - {user.username}
            Ваш новый пароль - {data['new_password1']}
        '''
        send_mail(
            subject,
            content,
            settings.EMAIL_HOST_USER,
            [f'{user.email}']
        )
        return super().form_valid(form)


class PasswordChangeDoneView(views.PasswordChangeDoneView):
    template_name = 'users/registration/password_change_done.html'


class PasswordResetConfirmView(views.PasswordResetConfirmView):
    template_name = 'users/registration/password_reset_confirm.html'
