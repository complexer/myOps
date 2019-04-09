from django.shortcuts import render
from .utils import *
from .forms import UploadFileForm
from .models import *


def repo_list(request):
    repos = Repo.objects.all()
    context = {}
    context['repos'] = repos
    return render(request, 'storage/repo_list.html', context)

def repo_create(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            app = request.POST.get('app')
            save_dir = handle_uploaded_file(request.FILES['file'],app)
            repo_init(save_dir)
            repo = Repo(name=app, path=save_dir)
            repo.save()

            return render(request, 'storage/ok.html', context={})
    else:
        forms = UploadFileForm()
        context = {}
        context['forms'] = forms
        return render(request, 'storage/upload.html', context)

def repo_show(request, repo_name):
    repo = Repo.objects.get(name=repo_name)
    repo_handle = RepoHandle(repo.path)
    files, type = repo_handle.repo_search(repo_handle.head_commit.tree.hexsha)
    context = {}
    context['files'] = files
    context['repo_name'] = repo_name
    if type == "tree":
        context['file_type'] = 'tree'
        context['forms'] = UploadFileForm()
        return render(request, 'storage/repo_show.html', context)
    else:
        raise Exception("Error Type!!!")


def file_show(request, repo_name, hexsha):
    repo = Repo.objects.get(name=repo_name)
    repo_handle = RepoHandle(repo.path)
    files, type = repo_handle.repo_search(hexsha)
    context = {}
    context['files'] = files
    context['repo_name'] = repo_name
    context['parent_dir_hexsha'] = hexsha
    if type == "tree":
        context['file_type'] = 'tree'
        context['forms'] = UploadFileForm()
        return render(request, 'storage/repo_show.html', context)
    elif type == "blob":
        context['file_type'] = 'blob'
        return render(request, 'storage/repo_show.html', context)
    else:
        raise Exception("Error Type!!!")


def repo_file_upload(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_name = request.POST.get('app')
            parent_dir_hexsha = request.POST.get('parent_dir_hexsha')
            repo_name = request.POST.get('repo_name')
            repo_handle = RepoHandle(Repo.objects.get(name=repo_name).path)


def tree_show(requset, repo_name, commit=None):
    repo = Repo.objects.get(name=repo_name)
    tree_handle = TreeHandle(repo.path, commit)
    context = {}
    context['repo_name'] = repo_name
    context['trees'] = tree_handle.tree.trees
    context['blobs'] = tree_handle.tree.blobs
    context['commit'] = commit
    return render(requset, 'storage/tree_show.html', context)

def tree_file_show(request, repo_name, file_path, commit=None):
    repo = Repo.objects.get(name=repo_name)
    tree_handle = TreeHandle(repo.path, commit)
    context = {}
    context['commit'] = commit

    if tree_handle.tree[file_path].type == 'tree':
        context['repo_name'] = repo_name
        context['trees'] = tree_handle.tree[file_path].trees
        context['blobs'] = tree_handle.tree[file_path].blobs
    else:
        #data_stream获取数据\r\n如何在网页站示
        context['file_content'] = tree_handle.tree[file_path].data_stream.read()
        # context['file_content'], type = RepoHandle(repo.path).repo_search(tree_handle.tree[file_path].hexsha)
    return render(request, 'storage/tree_show.html', context)

