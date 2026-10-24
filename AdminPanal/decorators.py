from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect("Login")

        if not request.user.is_admin:
            messages.error(request, "You are not authorized to access the admin panel.")
            return redirect("Home")

        return view_func(request, *args, **kwargs)

    return wrapper