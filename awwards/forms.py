from awwards.models import Project
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    full_name = forms.CharField(max_length=50, required=False)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('full_name', 'username','email', 'password1', 'password2', )

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['user','profile','date']