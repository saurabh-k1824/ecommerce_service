
from django.contrib import admin
from django.urls import path

from django.urls import path

from auth_service.views.login import LoginView
from auth_service.views.refresh_views import RefreshTokenView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", RefreshTokenView.as_view()),
    
]

