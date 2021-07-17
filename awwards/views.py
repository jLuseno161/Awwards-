from awwards.models import Profile, Project
from awwards.forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate


@login_required(login_url='/accounts/login/')
def index(request):
    profile = Profile.objects.all()
    return render(request,'index.html',{"profile":profile})
    
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
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required(login_url='/accounts/login/')    
def profile(request):
    current_user= request.user
    projects= Project.objects.filter(profile=current_user.id).all
    return render(request, 'registration/profile.html',{"projects":projects} )

def profileEndpoint(request):
    pass

def projectsEndpoint(request):
    pass