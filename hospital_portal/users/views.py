from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

from .forms import ProfileForm, UserRegisterForm
from .models import Profile


def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            username = user_form.cleaned_data.get('username')
            email = user_form.cleaned_data.get('email')

            if User.objects.filter(username=username).exists():
                messages.error(request, "⚠️ Username already exists. Please choose another.")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "⚠️ Email already exists. Try with another email.")
            else:
                user = user_form.save()
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()

                messages.success(request, "🎉 Account created successfully! Please login.")
                return redirect('login')
    else:
        user_form = UserRegisterForm()
        profile_form = ProfileForm()

    return render(request, 'users/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            profile = Profile.objects.get(user=user)
            if profile.user_type == 'doctor':
                return redirect('doctor_dashboard')
            elif profile.user_type == 'patient':
                return redirect('patient_dashboard')
            else:
                messages.warning(request, "⚠️ Unknown user type.")
                return redirect('login')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


@login_required
def doctor_dashboard(request):
    profile = request.user.profile
    return render(request, 'users/doctor_dashboard.html', {
        'user': request.user,
        'profile': profile
    })


@login_required
def patient_dashboard(request):
    profile = request.user.profile
    return render(request, 'users/patient_dashboard.html', {
        'user': request.user,
        'profile': profile
    })


@login_required
def dashboard(request):
    profile = request.user.profile
    if profile.user_type == 'doctor':
        return redirect('doctor_dashboard')
    elif profile.user_type == 'patient':
        return redirect('patient_dashboard')
    else:
        return redirect('login')  # fallback