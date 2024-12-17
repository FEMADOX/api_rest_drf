from django.urls import path

from api_auth.views import LoginView, SignUpView, UserView

urlpatterns = [
    path("signup/", SignUpView.as_view()),
    path("login/", LoginView.as_view()),
    path("user/<lookup_value>", UserView.as_view()),
]
