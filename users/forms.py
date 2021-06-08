from django.contrib.auth import forms
from django.contrib.auth import get_user_model


User = get_user_model()


class CreationForm(forms.UserCreationForm):
    class Meta(forms.UserCreationForm.Meta):
        model = User
        fields = ("first_name", "username", "email")

    def __init__(self, *args, **kwargs):
        super(forms.UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].error_messages = '''
            Пользователь с таким акаунтом уже существует!
        '''
        self.fields['password2'].error_messages = 'Пароли не совпадают.'

    def clean_email(self):
        mail = self.cleaned_data['email']
        if User.objects.filter(email__iexact=mail).exists():
            raise forms.ValidationError(
                'Пользователь с таким "email" уже существует!'
            )
        return mail


class PasswordResetForm(forms.PasswordResetForm):

    def clean_email(self):
        mail = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=mail).exists():
            raise forms.ValidationError(
                'Пользователь с таким "email" не существует!'
            )
        return mail
