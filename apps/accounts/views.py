from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile

from django.http import HttpResponse
from cineast_core.ratelimit import check_rate_limit, record_rate_limit_attempt, reset_rate_limit

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        if check_rate_limit(request, 'auth_login', max_attempts=10, timeout=900):
            messages.error(request, "Too many login attempts. Please wait 15 minutes before trying again.")
            return render(request, 'accounts/login.html', status=429)

        username_input = (request.POST.get('username') or '').strip()
        password = request.POST.get('password') or ''
        next_url = request.POST.get('next') or 'home'

        # Support login with either username or email
        if '@' in username_input:
            user_by_email = User.objects.filter(email__iexact=username_input).first()
            if user_by_email:
                username_input = user_by_email.username

        user = authenticate(request, username=username_input, password=password)
        if user is not None:
            reset_rate_limit(request, 'auth_login')
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect(next_url)
        else:
            record_rate_limit_attempt(request, 'auth_login', timeout=900)
            messages.error(request, "Invalid username or password.")
    return render(request, 'accounts/login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        if check_rate_limit(request, 'auth_register', max_attempts=10, timeout=900):
            messages.error(request, "Too many registration attempts. Please wait 15 minutes before trying again.")
            return render(request, 'accounts/register.html', status=429)

        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2') or request.POST.get('password_confirm', '')

        if not username or not email or not password:
            messages.error(request, "All fields are required.")
            return render(request, 'accounts/register.html')

        if password != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'accounts/register.html')

        if User.objects.filter(username__iexact=username).exists():
            messages.error(request, "Username is already taken.")
            return render(request, 'accounts/register.html')

        if User.objects.filter(email__iexact=email).exists():
            messages.error(request, "Email is already registered.")
            return render(request, 'accounts/register.html')

        user = User.objects.create_user(username=username, email=email, password=password)
        reset_rate_limit(request, 'auth_register')
        login(request, user)
        request.session['show_new_user_tour'] = True
        messages.success(request, f"Welcome to anything..., {user.username}! Your account has been created.")
        return redirect('home')


    return render(request, 'accounts/register.html')


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')

def user_profile_view(request, username):
    profile_user = get_object_or_404(User.objects.select_related('profile'), username=username)
    ratings = profile_user.ratings.select_related('entity__category').all()[:20]
    reviews = profile_user.reviews.select_related('entity__category', 'rating').all()[:20]
    contributions = profile_user.contributions.select_related('entity').all()[:20]
    created_entities = profile_user.created_entities.select_related('category').all()[:20]

    context = {
        'profile_user': profile_user,
        'ratings': ratings,
        'reviews': reviews,
        'contributions': contributions,
        'created_entities': created_entities,
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def edit_profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        bio = request.POST.get('bio', '').strip()
        avatar = request.FILES.get('avatar')
        
        if avatar:
            if avatar.size > 5 * 1024 * 1024:
                messages.error(request, "Avatar image must be under 5MB.")
                return render(request, 'accounts/edit_profile.html', {'profile': profile})
            try:
                from PIL import Image
                img = Image.open(avatar)
                img.verify()
                avatar.seek(0)
            except Exception:
                messages.error(request, "Invalid or corrupted image file.")
                return render(request, 'accounts/edit_profile.html', {'profile': profile})
            profile.avatar = avatar

        profile.bio = bio
        profile.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('user_profile', username=request.user.username)

    return render(request, 'accounts/edit_profile.html', {'profile': profile})

