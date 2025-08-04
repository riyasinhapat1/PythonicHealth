from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# ✅ FIX: Use relative import instead of full path
from .forms import ProfileForm, UserRegisterForm

def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            username = user_form.cleaned_data.get('username')
            email = user_form.cleaned_data.get('email')

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists. Please choose another.")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists. Try with another email.")
            else:
                user = user_form.save(commit=False)
                user.set_password(user_form.cleaned_data['password'])
                user.save()

                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()

                messages.success(request, "Account created successfully. Please login.")
                return redirect('login')
    else:
        user_form = UserRegisterForm()
        profile_form = ProfileForm()

    return render(request, 'users/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


@login_required
def dashboard(request):
    profile = request.user.profile
    if profile.user_type == 'patient':
        return render(request, 'users/patient_dashboard.html')
    else:
        return render(request, 'users/doctor_dashboard.html')
