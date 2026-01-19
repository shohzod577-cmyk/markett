"""
User authentication and profile views.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods

from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm, AddressForm
from .models import Address


@require_http_methods(["GET", "POST"])
def register_view(request):
    """
    User registration view.
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email'].lower()
            user.username = user.email
            user.set_password(form.cleaned_data['password'])
            user.save()

            login(request, user)
            messages.success(request, 'Welcome to Market!  Your account has been created.')

            from core.services.email import EmailService
            EmailService().send_welcome_email(user)

            return redirect('home')
    else:
        form = UserRegistrationForm()

    return render(request, 'users/register.html', {'form': form})


@require_http_methods(["GET", "POST"])
def login_view(request):
    """
    User login view.
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, username=email, password=password)

            if user is not None:
                if user.is_blocked:
                    messages.error(request, 'Your account has been blocked.')
                else:
                    login(request, user)
                    messages.success(request, f'Welcome back, {user.first_name or user.email}!')

                    next_url = request.GET.get('next', 'home')
                    return redirect(next_url)
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = UserLoginForm()

    return render(request, 'users/login.html', {'form': form})


@login_required
def logout_view(request):
    """
    User logout view.
    """
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def profile_view(request):
    """
    User profile management view.
    """
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('users:profile')
    else:
        form = UserProfileForm(instance=request.user)

    context = {
        'form': form,
        'addresses': request.user.addresses.all(),
        'orders': request.user.orders.all()[: 10],
    }

    return render(request, 'users/profile.html', context)


@login_required
def add_address_view(request):
    """
    Add new address view.
    """
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, 'Address added successfully.')
            return redirect('users:profile')
    else:
        form = AddressForm()

    return render(request, 'users/add_address.html', {'form': form})


@login_required
def edit_address_view(request, address_id):
    """
    Edit existing address view.
    """
    address = Address.objects.get(id=address_id, user=request.user)

    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, 'Address updated successfully.')
            return redirect('users:profile')
    else:
        form = AddressForm(instance=address)

    return render(request, 'users/edit_address.html', {'form': form, 'address': address})


@login_required
def delete_address_view(request, address_id):
    """
    Delete address view.
    """
    address = Address.objects.get(id=address_id, user=request.user)
    address.delete()
    messages.success(request, 'Address deleted successfully.')
    return redirect('users:profile')