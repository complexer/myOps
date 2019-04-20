from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.repo_list, name='repo_list'),

    path('repo_create/', views.repo_create, name='repo_create'),

    path('upload/', views.ws_file_upload, name='ws_file_upload'),

    path('ws_file_update/', views.ws_file_update, name='ws_file_update'),

    path('get_head_ws_diff/<str:repo_name>/', views.get_head_ws_diff, name='get_head_ws_diff'),
    path('get_commit_diff/<str:repo_name>/<str:commit_base_id>/<str:commit_compare_id>', views.get_commit_diff, name='get_commit_diff'),

    path('repo/<str:repo_name>/commit_history/', views.commit_history, name='commit_history'),
    re_path(r'^tree/(?P<repo_name>.*)/workspace$', views.ws_show, name='ws_show'),
    re_path(r'^tree/(?P<repo_name>.*)/workspace/(?P<file_path>.*)$', views.ws_file_show, name='ws_file_show'),

    #master这两个考虑不用，直接展示工作区，master的文件内容直接通过下面的commit来显示和查看
    re_path(r'^tree/(?P<repo_name>.*)/master$', views.tree_show, name='tree_show'),
    re_path(r'^tree/(?P<repo_name>.*)/master/(?P<file_path>.*)$', views.tree_file_show, name='tree_file_show'),

    re_path(r'^tree/(?P<repo_name>.*)/(?P<commit>[0-9a-z]{40})$', views.tree_show, name='tree_last_show'),
    re_path(r'^tree/(?P<repo_name>.*)/(?P<commit>[0-9a-z]{40})/(?P<file_path>.*)$', views.tree_file_show, name='tree_last_file_show'),
]
