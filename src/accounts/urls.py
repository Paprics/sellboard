from django.contrib.auth.views import LogoutView
from django.urls import path
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.UserRegisterView.as_view(), name='signup'),
    # path("verify/<uidb64>/<token>/", views.VerifyEmailView.as_view(), name="verify_email"),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('chenge/', views.ChangePasswordView.as_view(), name='change_password'),
    # path('reset/')


]
