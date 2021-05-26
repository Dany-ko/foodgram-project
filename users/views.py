from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import views

from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy("login")
    template_name = "users/signup.html"
