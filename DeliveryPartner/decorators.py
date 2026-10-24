from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def delivey_partner_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect("DeliveryPartnerLogin")

        if not request.user.is_delivery_partner:
            messages.error(request, "You are not authorized to access the delivery partners panel.")
            return redirect("Home")

        return view_func(request, *args, **kwargs)

    return wrapper