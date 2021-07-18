from awwards.models import Profile, Project
from django.contrib.auth.models import User
from awwards.forms import ProjectForm, RatingsForm, SignUpForm, UpdateProfileForm, UpdateUserForm
from django.contrib.auth.forms import AuthenticationForm
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.urls import reverse

# api urls

from .models import Profile, Project, Rates
from .serializers import ProfileSerializer, ProjectSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


def index(request):
    profile = Profile.objects.all()
    projects = Project.objects.all()
    return render(request, 'index.html', {"profile": profile, "projects": projects})


def signup(request):
    print('here')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # form.save()
            # username = form.cleaned_data.get('username')
            # raw_password = form.cleaned_data.get('password1')
            # user = authenticate(username=username, password=raw_password)
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.birth_date = form.cleaned_data.get('full_name')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)

            login(request, user)
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration/registration_form.html', {'form': form})


@login_required(login_url='/accounts/login/')
def profile(request):
    current_user = request.user
    projects = Project.objects.filter(user=current_user.id).all
    return render(request, 'registration/profile.html', {"projects": projects})


@login_required(login_url='/accounts/login/')
def update_profile(request, id):

    obj = get_object_or_404(Profile, user_id=id)
    obj2 = get_object_or_404(User, id=id)
    form = UpdateProfileForm(request.POST or None, instance=obj)
    form2 = UpdateUserForm(request.POST or None, instance=obj2)
    if form.is_valid() and form2.is_valid():
        form.save()
        form2.save()
        return HttpResponseRedirect("/profile")

    return render(request, "registration/update_profile.html", {"form": form, "form2": form2})


@login_required(login_url='/accounts/login')
def post_project(request):
    current_user = request.user
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            post_project = form.save(commit=False)
            post_project.user = current_user
            post_project.save()
            return redirect('index')
    else:
        form = ProjectForm()
    return render(request, 'projects.html', {"form": form})


@login_required(login_url='/accounts/login')
def project(request, id):
    project = Project.objects.get(id=id)
    reviews = Rates.objects.all()
    return render(request, 'viewProject.html', {"project": project, "reviews": reviews})


@login_required(login_url='/accounts/login')
def view_project(request, id):
    project = Project.objects.get(id=id)
    # ratings = Rates.objects.filter(user=request.user, project=project).first()
    ratings = Rates.objects.all()
    rating_status = None
    if ratings is None:
        rating_status = False
    else:
        rating_status = True
    if request.method == 'POST':
        form = RatingsForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.project = project
            review.save()
            post_ratings = Rates.objects.filter(project=project)

            design_ratings = [d.design for d in post_ratings]
            design_average = sum(design_ratings) / len(design_ratings)

            usability_ratings = [us.usability for us in post_ratings]
            usability_average = sum(usability_ratings) / len(usability_ratings)

            content_ratings = [content.content for content in post_ratings]
            content_average = sum(content_ratings) / len(content_ratings)

            score = (design_average + usability_average + content_average) / 3
            print(score)
            review.design = round(design_average, 2)
            review.usability = round(usability_average, 2)
            review.content = round(content_average, 2)
            review.average = round(score, 2)
            review.save()
            return HttpResponseRedirect(reverse('viewProject', args=(project.id,)))
    else:
        form = RatingsForm()
    params = {
        'project': project,
        'form': form,
        'rating_status': rating_status,
        'reviews': ratings,
        
    }
    return render(request, 'viewProject.html', params)


class ProfileList(APIView):
    """
    List all snippets, or create a new snippet.
    """

    def get(self, request, format=None):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)


class ProjectList(APIView):
    """
    List all snippets, or create a new snippet.
    """

    def get(self, request, format=None):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)
