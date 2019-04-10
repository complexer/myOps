from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.repo_list, name='repo_list'),
    path('repo_create/', views.repo_create, name='repo_create'),


    # path('repo_show/<str:repo_name>/', views.repo_show, name='repo_show'),
    # path('file_show/<str:repo_name>/<str:hexsha>/', views.file_show, name='file_show'),
    # path('repo_file_upload/', views.repo_file_upload, name='repo_file_upload'),
    re_path(r'^tree/(?P<repo_name>.*)/workspace$', views.ws_show, name='ws_show'),
    re_path(r'^tree/(?P<repo_name>.*)/workspace/(?P<file_path>.*)$', views.ws_file_show, name='ws_file_show'),

    re_path(r'^tree/(?P<repo_name>.*)/master$', views.tree_show, name='tree_show'),
    re_path(r'^tree/(?P<repo_name>.*)/master/(?P<file_path>.*)$', views.tree_file_show, name='tree_file_show'),
    re_path(r'^tree/(?P<repo_name>.*)/(?P<commit>[0-9a-z]{40})$', views.tree_show, name='tree_last_show'),
    re_path(r'^tree/(?P<repo_name>.*)/(?P<commit>[0-9a-z]{40})/(?P<file_path>.*)$', views.tree_file_show, name='tree_last_file_show'),
]
