from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name = 'index'),
    path('signup/', views.signup, name='signup'),
    path('profile/',views.profile, name='profile'),
    path('upload/',views.post_project,name='post_prj'),
    path('project_details/(?P<id>\d+)', views.view_project, name='viewProject'),



    #api endpoints

    path('api/v1/profile',views.ProfileList.as_view(),name='profileEndpoint'),
    path('api/v1/projects',views.ProjectList.as_view(),name='projectsEndpoint')
]