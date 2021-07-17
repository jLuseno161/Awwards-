from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name = 'index'),
    path('signup/', views.signup, name='signup'),
    path('profile',views.profile, name='profile'),

    #api endpoints

    path('api/v1/profile',views.profileEndpoint,name='profileEndpoint'),
    path('api/v1/projects',views.projectsEndpoint,name='projectsEndpoint')
]