"""
Dashboard access decorators.
"""
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def admin_required(view_func):
    """
    Decorator to restrict access to admin users only.
    """

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please login to access the dashboard.')
            return redirect('users:login')

        if not (request.user.is_staff or request.user.is_superuser):
            messages.error(request, 'You do not have permission to access the dashboard.')
            return redirect('home')

        return view_func(request, *args, **kwargs)

    return wrapper