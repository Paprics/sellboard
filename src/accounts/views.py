from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.core.mail import send_mail
from .forms import UserRegistrationForm, LoginForm, ChangePasswordForm


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

class ChangePasswordView(FormView):
    template_name = "change_password.html"
    form_class = ChangePasswordForm
    success_url = reverse_lazy("core:home")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        password = form.cleaned_data['new_password1']
        user = form.save()
        user = authenticate(username=user.username, password=password)
        login(self.request, user)
        return super().form_valid(form)
