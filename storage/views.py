from django.shortcuts import render,redirect
from django.http import JsonResponse
from .utils import *
from .forms import UploadFileForm
from .models import *
from django.urls import reverse
import  json


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

def tree_show(requset, repo_name, commit=None):
    '''
    给commit log用展示根
    :param requset:
    :param repo_name:
    :param commit:
    :return:
    '''
    repo = Repo.objects.get(name=repo_name)
    tree_handle = TreeHandle(repo.path, commit)
    context = {}
    context['repo_name'] = repo_name
    context['trees'] = tree_handle.tree.trees
    context['blobs'] = tree_handle.tree.blobs
    context['commit'] = commit
    return render(requset, 'storage/tree_show.html', context)

def tree_file_show(request, repo_name, file_path, commit=None):
    '''
    给commit log用展示文件
    :param request:
    :param repo_name:
    :param file_path:
    :param commit:
    :return:
    '''
    repo = Repo.objects.get(name=repo_name)
    tree_handle = TreeHandle(repo.path, commit)
    context = {}

    if tree_handle.tree[file_path].type == 'tree':
        context['repo_name'] = repo_name
        context['trees'] = tree_handle.tree[file_path].trees
        context['blobs'] = tree_handle.tree[file_path].blobs
    else:
        '''
        data_stream获取到的数据是rb模式读取的，需要互相转换下(python中string前加r、b、u的意思需要了解下)
        在 Python3 中，bytes 和 str 的互相转换方式是
        str.encode('utf-8')
        bytes.decode('utf-8')
        '''
        context['file_content'] = tree_handle.tree[file_path].data_stream.read().decode('utf-8')
        # context['file_content'], type = RepoHandle(repo.path).repo_search(tree_handle.tree[file_path].hexsha)
    return render(request, 'storage/tree_show.html', context)

def ws_show(request, repo_name):
    '''
    工作区根目录展示
    :param request:
    :param repo_name:项目名称
    :return:
    '''
    repo = Repo.objects.get(name=repo_name)
    files = os.listdir(repo.path)
    form = UploadFileForm(request.POST, request.FILES)
    context = {}
    context['files'] = files
    context['repo_name'] = repo_name
    context['form'] = form
    return render(request, 'storage/ws_show.html', context)



def ws_file_show(request, repo_name, file_path):
    '''
    工作区下面的文件及目录展示
    :param request:
    :param repo_name:
    :param file_path:
    :return:
    '''
    repo = Repo.objects.get(name=repo_name)
    target_file = repo.path+file_path
    is_dir = os.path.isdir(target_file)
    print(file_path)
    context = {}
    context['repo_name'] = repo_name

    if is_dir:
        form = UploadFileForm(request.POST, request.FILES)
        context['form'] = form
        files = os.listdir(target_file)
        context['file_path'] = file_path +'/'
        context['files'] = files
        return render(request, 'storage/ws_show.html', context)
    else:
        context['file_path'] = file_path
        with open(target_file, 'r', encoding='utf-8') as f:
            context['file_content'] = f.read()
        #两种显示格式一种是文本框，一种是raw
        return render(request, 'storage/ws_filecontent_show.html', context)
        # return render(request, 'storage/raw.html', context)

def ws_file_upload(request):
    '''
    文件上传
    :param request:
    :return:
    '''
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            repo = Repo.objects.get(name=request.POST.get('repo_name'))
            file = request.FILES['file']
            file_path = request.POST.get('file_path','')
            save_target = repo.path+file_path+file.name
            if os.path.exists(save_target):
                add_flage = False
            else:
                add_flage = True
            with open(save_target, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            if add_flage:
                tree = TreeHandle(repo.path)
                tree.index_add_file()
            return redirect(request.POST.get('from', reverse('repo_list')))


def commit_history(request, repo_name):
    '''
    展示commit log
    :param request:
    :param repo_name:
    :return:
    '''
    repo_info = Repo.objects.get(name=repo_name)
    repo = git.Repo(repo_info.path)
    commit_logs = repo.iter_commits('master', max_count=10, skip=0)
    context = {}
    context['commit_logs'] = commit_logs
    context['repo_name'] = repo_name
    return render(request, 'storage/commit_log.html', context)


def ws_file_update(request):
    if request.method == 'POST':
        repo_name = request.POST.get('repo_name')
        file_path = request.POST.get('file_path')
        file_content = request.POST.get('file_content').replace("\n","")
        repo_info = Repo.objects.get(name=repo_name)
        target_file = repo_info.path+file_path
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(file_content)
        return redirect(request.POST.get('from', reverse('repo_list')))


def get_head_ws_diff(request, repo_name):
    repo_info = Repo.objects.get(name=repo_name)
    tree = TreeHandle(repo_info.path)
    diff_data = tree.get_head_ws_diff()
    datas = {}
    i = 0
    for dd in diff_data:
        data = {}
        data['change_type'] = dd.change_type
        data['file_name'] = dd.a_path
        datas['%s' % i] = data
    return JsonResponse(datas)