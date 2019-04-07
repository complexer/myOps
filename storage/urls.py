from django.urls import path
from . import views

urlpatterns = [
    path('', views.repo_list, name='repo_list'),
    path('repo_create/', views.repo_create, name='repo_create'),
    path('repo_show/<str:repo_name>/', views.repo_show, name='repo_show'),
]
