from django.urls import path
from .views import *

urlpatterns = [
    path("login/", login_view, name="Login"),
    path("register/", register_view, name="Register"),
    path("logout/", logout_view, name="Logout"),
]