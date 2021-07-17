from awwards.models import Profile, Project
from awwards.forms import ProjectForm, SignUpForm
from django.contrib.auth.forms import AuthenticationForm
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate

#api urls

from .models import Profile,Project
from .serializers import ProfileSerializer,ProjectSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


@login_required(login_url='/accounts/login/')
def index(request):
    profile = Profile.objects.all()
    projects = Project.objects.all()
    return render(request,'index.html',{"profile":profile,"projects":projects})
    
def signup(request):
    print('here')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required(login_url='/accounts/login/')    
def profile(request):
    current_user= request.user
    projects= Project.objects.filter(profile=current_user.id).all
    return render(request, 'registration/profile.html',{"projects":projects} )

@login_required(login_url='/accounts/login')
def post_project(request):
	current_user = request.user
	if request.method == 'POST':
		form = ProjectForm(request.POST,request.FILES)
		if form.is_valid():
			new_project = form.save(commit=False)
			new_project.user = current_user
			new_project.save()
			return redirect('index')
	else:
			form = ProjectForm()
	return render(request, 'projects.html',{"form":form})


# @login_required(login_url='/accounts/login')
# def show_projects(request,id):
#     project = Project.objects.get(id = id)

#     return render(request, 'project_details.html',{"project":project}) 


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
