from django.urls import path

from api_auth.views import LoginView, UserView


urlpatterns = [
    path('user/', UserView.as_view()),
    path('login/', LoginView.as_view()),
]
