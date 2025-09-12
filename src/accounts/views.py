from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.core.mail import send_mail
from .forms import UserRegistrationForm, LoginForm


class UserRegisterView(FormView):
    template_name = "registration.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_verified  = False
        user.save()

        #TODO
        # Отправка письма
        # send_mail(
        #     subject="Confirm your email",
        #     message="Click the link to verify your account...",
        #     from_email="noreply@example.com",
        #     recipient_list=[user.email],
        # )

        return super().form_valid(form)

class LoginView(FormView):
    template_name = "login-temp.html"
    success_url = reverse_lazy("core:home")
    form_class = LoginForm

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)
