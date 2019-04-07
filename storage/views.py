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
    '''
    再加一个参数，如果为空就是返回repo.head.commit的tree?
    :param request:
    :param repo_name:
    :return:
    '''
    repo = Repo.objects.get(name=repo_name)
    repo_handle = RepoHandle(repo.path)
    files, type = repo_handle.repo_search(repo_handle.head_commit.tree.hexsha)
    context = {}
    context['files'] = files
    context['repo_name'] = repo_name
    if type == "tree":
        return render(request, 'storage/repo_show.html', context)
    else:
        raise Exception("Error Type!!!")


def file_show(request, repo_name, hexsha):
    repo = Repo.objects.get(name=repo_name)
    repo_handle = RepoHandle(repo.path)
    files, type = repo_handle.repo_search(hexsha)
    context = {}
    if type == "tree":
        pass
    elif type == "blob":
        pass
    else:
        raise Exception("Error Type!!!")


