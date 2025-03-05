from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Count  # ✅ Import Count function
from .models import Organization

from .forms import (
    CreateProjectForm,
    RegisterForm,
    UserUpdateForm,
    ProfileUpdateForm, ProfileImageForm,
)
def homepage_view(request):
    """Loads the homepage with featured organizations."""
    organizations = Organization.objects.annotate(
        project_count=Count("projects")
    ).filter(project_count__gt=0)

    print("🔍 Organizations Found:", organizations)  # Debugging line

    return render(request, "hub/homepage.html", {"organizations": organizations})

from django.db.models import Count
from django.shortcuts import render
from myapp.models import Organization

def homepage_view(request):
    """Loads the homepage with featured organizations."""
    organizations = Organization.objects.annotate(project_count=Count("projects")).filter(project_count__gt=0)

    print("🔍 Organizations Sent to Template:", organizations)  # Debugging

    return render(request, "hub/homepage.html", {"organizations": organizations})

def project_detail(request, pk):
    """View for displaying project details."""
    project = get_object_or_404(Project, pk=pk)
    return render(request, "hub/project_detail.html", {"project": project})

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


from django.http import JsonResponse
from .models import Project

def filter_projects(request):
    projects = Project.objects.filter(approved=True)

    type_filter = request.GET.get("type", "")
    country_filter = request.GET.get("country", "")
    deadline_filter = request.GET.get("deadline", "")

    if type_filter and type_filter != "All":
        projects = projects.filter(type=type_filter)
    if country_filter:
        projects = projects.filter(country=country_filter)
    if deadline_filter:
        projects = projects.filter(deadline__lte=deadline_filter)

    # ✅ Always return all approved projects if no filters are applied
    project_list = [
        {
            "id": project.id,
            "name": project.name,
            "country": project.country,
            "deadline": project.deadline.strftime("%Y-%m-%d"),
            "submitted_by": project.submitted_by,
        }
        for project in projects
    ]

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

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile, Certification, Badge
from .forms import UserUpdateForm, ProfileUpdateForm


@login_required
def profile(request):
    """Displays and updates the user profile."""
    user_profile, created = Profile.objects.get_or_create(user=request.user)
    certifications = Certification.objects.filter(user=request.user)
    badges = Badge.objects.filter(users=request.user)

    if request.method == "POST":
        # Check if the profile image is being updated
        if "profile_image" in request.FILES:
            image_form = ProfileImageForm(request.POST, request.FILES, instance=user_profile)
            if image_form.is_valid():
                image_form.save()
                messages.success(request, "Profile picture updated successfully!")
                return redirect("profile")
            else:
                messages.error(request, "Error updating profile picture. Check the details.")

        elif "remove_picture" in request.POST:
            user_profile.profile_image = "default.png"
            user_profile.save()
            messages.success(request, "Profile picture removed successfully!")
            return redirect("profile")

        else:
            # Handle full profile update
            user_form = UserUpdateForm(request.POST, instance=request.user)
            profile_form = ProfileUpdateForm(request.POST, instance=user_profile)
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

def filter_projects_api(request):
    projects = Project.objects.filter(approved=True)

    type_filter = request.GET.get("type", "")
    country_filter = request.GET.get("country", "")
    deadline_filter = request.GET.get("deadline", "")

    if type_filter and type_filter != "All":
        projects = projects.filter(type=type_filter)
    if country_filter:
        projects = projects.filter(country=country_filter)
    if deadline_filter:
        projects = projects.filter(deadline__lte=deadline_filter)

    project_list = list(projects.values("id", "name", "country", "deadline", "submitted_by", "approved"))
    return JsonResponse(project_list, safe=False)
