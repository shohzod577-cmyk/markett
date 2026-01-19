from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from .tokens import verification_token
from django.urls import reverse


def register_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email'].lower()
            user.username = form.cleaned_data.get('username') or user.email
            user.set_password(form.cleaned_data['password'])
            user.save()
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = verification_token.make_token(user)
            verify_url = request.build_absolute_uri(
                reverse('users:verify', args=[uid, token])
            )
            context = {'user': user, 'verify_url': verify_url, 'site_name': getattr(settings, 'SITE_NAME', 'Market')}
            subject = f"Verify your {context['site_name']} account"
            text = render_to_string('emails/verify_email.txt', context)
            html = render_to_string('emails/verify_email.html', context)
            email = EmailMultiAlternatives(subject, text, settings.DEFAULT_FROM_EMAIL, [user.email])
            email.attach_alternative(html, 'text/html')
            email.send(fail_silently=True)

            login(request, user)
            messages.success(request, 'Account created — check your email to verify your address')
            return redirect('/')
    else:
        initial = {}
        if request.GET.get('username'):
            initial['username'] = request.GET.get('username')
        form = UserRegistrationForm(initial=initial)
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['email'].lower(), password=form.cleaned_data['password'])
            if user:
                login(request, user)
                next_url = request.POST.get('next') or request.GET.get('next')
                return redirect(next_url or '/')
            messages.error(request, 'Invalid credentials')
    else:
        form = UserLoginForm()
    next_url = request.GET.get('next') or request.POST.get('next') or ''
    return render(request, 'users/login.html', {'form': form, 'next_url': next_url})


def logout_view(request):
    logout(request)
    return redirect('/')


def verify_email_view(request, uidb64, token):
    """Verify email address from token link."""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        from django.contrib.auth import get_user_model

        User = get_user_model()
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user is not None and verification_token.check_token(user, token):
        user.is_verified = True
        user.save()
        messages.success(request, 'Email verified successfully.')
        return redirect('users:login')

    messages.error(request, 'Verification link is invalid or expired.')
    return redirect('users:register')
