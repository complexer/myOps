from django.urls import path
from . import views

urlpatterns = [
    path('', views.repo_list, name='repo_list'),
    path('repo_create/', views.repo_create, name='repo_create'),
    path('repo_show/<str:repo_name>/', views.repo_show, name='repo_show'),
    path('file_show/<str:repo_name>/<str:hexsha>/', views.file_show, name='file_show'),
    path('repo_file_upload/', views.repo_file_upload, name='repo_file_upload'),


]
