from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

from .models import Profile, Certification, Badge, Project
from .forms import (
    CreateProjectForm,
    RegisterForm,
    UserUpdateForm,
    ProfileUpdateForm,
)


def homepage_view(request):
    return render(request, "hub/homepage.html")


def project_detail(request, pk):
    """View for displaying project details."""
    project = get_object_or_404(Project, pk=pk)
    return render(request, "hub/project_detail.html", {"project": project})


from django.contrib import messages

from django.contrib import messages

def register(request):
    """Handles user registration and ensures a profile is created."""
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            # ✅ Ensure profile is created
            Profile.objects.get_or_create(user=user)

            messages.success(request, "Registration successful! You can now log in.")
            return redirect("auth")
        else:
            print(form.errors)  # 🔍 Debugging: Print errors in the terminal
            for error in form.errors.values():
                messages.error(request, error)  # ✅ Show errors on the UI

    else:
        form = RegisterForm()

    return render(request, "hub/auth.html", {"form": form})


def logout_view(request):
    """Logs the user out and redirects to homepage."""
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("/")


def filter_projects(request):
    """Filters projects based on query parameters."""
    projects = Project.objects.filter(approved=True)

    type_filter = request.GET.get("type", "")
    country_filter = request.GET.get("country", "")
    deadline_filter = request.GET.get("deadline", "")

    if type_filter:
        projects = projects.filter(type=type_filter)
    if country_filter:
        projects = projects.filter(country=country_filter)
    if deadline_filter:
        projects = projects.filter(deadline__lte=deadline_filter)

    project_list = list(
        projects.values("id", "title", "country", "deadline", "submitted_by")
    )

    return JsonResponse(project_list, safe=False)


def filter_projects_view(request):
    """Renders the project filtering page."""
    return render(request, "hub/filter_projects.html")


@login_required
def suggest_project(request):
    """Allows logged-in users to suggest projects."""
    if request.method == "POST":
        form = CreateProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.submitted_by = request.user.username
            project.approved = request.user.is_staff  # Auto-approve if user is staff
            project.save()
            messages.success(request, "Project submitted successfully!")
            return redirect("/")
        else:
            messages.error(request, "Error submitting the project. Check your details.")
    else:
        form = CreateProjectForm()

    return render(request, "hub/suggest_project.html", {"form": form})


def project_list(request):
    """Displays a list of approved projects."""
    projects = Project.objects.filter(approved=True)
    return render(request, "hub/filter_projects.html", {"projects": projects})


@login_required
def profile(request):
    """Displays and updates the user profile."""
    user_profile, created = Profile.objects.get_or_create(user=request.user)
    certifications = Certification.objects.filter(user=request.user)
    badges = Badge.objects.filter(users=request.user)  # ✅ Correct ManyToMany lookup

    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=user_profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("profile")
        else:
            messages.error(request, "Error updating profile. Check your details.")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=user_profile)

    return render(
        request,
        "hub/profile.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
            "certifications": certifications,
            "badges": badges,
        },
    )


def award_badge(user, project):
    """Awards a badge to a user for completing a project."""
    badge_name = f"Completed {project.title}"
    badge, created = Badge.objects.get_or_create(name=badge_name)
    if not badge.users.filter(id=user.id).exists():
        badge.users.add(user)
        messages.success(user, f"You have earned a new badge: {badge_name}")
    else:
        messages.info(user, f"You already have the badge: {badge_name}")
