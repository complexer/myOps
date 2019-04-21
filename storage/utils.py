import os
import zipfile
import tarfile
import git
import shutil
from myops.settings import *

def handle_uploaded_file(f,app):
    save_dir = REPO_DIR + app + '/'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    file_path = save_dir + f.name
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    with zipfile.ZipFile(file_path) as z:
        z.extractall(save_dir)

    os.remove(file_path)
    return save_dir

def repo_init(path):
    repo = git.Repo.init(path, mkdir=True)
    index = repo.index
    index.add('*')
    res = index.commit(message='test')
    return res

def compress_file_handle(file, file_path):
    is_zip = zipfile.is_zipfile(file)
    is_tar = tarfile.is_tarfile(file)
    if is_zip is False & is_tar is False:
        return True
    else:
        if is_zip:
            with zipfile.ZipFile(file) as z:
                z.extractall(file_path)
        elif is_tar:
            with tarfile.open(file) as z:
                z.extractall(file_path)
    os.remove(file)

def delete_file(target_file):
    ls = os.listdir(target_file)
    for i in ls:
        if i == ".git":
            continue

        c_path = target_file + '/' + i
        if os.path.isdir(c_path):
            shutil.rmtree(c_path)
        else:
            os.remove(c_path)


class GitHandle(object):
    '''
    通过操作tree来获取文件
    repo = git.Repo(path)
    tree = repo.tree()
    tree['static/js/me.js']搜索文件
    '''

    def __init__(self, path, commit=None):
        self.repo = git.Repo(path)
        if commit is None:
            self.tree = self.repo.tree()
        else:
            self.tree = self.repo.tree(commit)

    def index_add_file(self):
        self.index = self.repo.index
        self.index.add('*')

    def get_head_ws_diff(self):
        return self.repo.head.commit.diff()


if __name__ == '__main__':

    # test = TreeHandle("../repository/test", '6822b3fa13d1c20249ef23764949771c52041735')
    # a = test.tree['views.py']
    # print(a)
    #

    # repo = git.Repo("../repository/test")
    # index = repo.index
    # a = index.diff(None)
    # print(a)


    # hc = repo.head.commit
    #head与暂存区比较git diff --name-status 615df673dc3e674cdbebdc4bd3812b69b6a38b97
    # a = hc.diff()
    # print(str(a[0].change_type)+'||'+str(a[0].a_path))

    # head与暂存区比较git diff --name-status 615df673dc3e674cdbebdc4bd3812b69b6a38b97
    # wdiff = hc.diff(None)
    # print(wdiff)

    #比较两个历史版本差异
    #git diff --name-status 8a90c2e03c1caf00c5189549f0af7393c51a9140 615df673dc3e674cdbebdc4bd3812b69b6a38b97
    # c = repo.commit('8a90c2e03c1caf00c5189549f0af7393c51a9140')
    # h = c.diff('615df673dc3e674cdbebdc4bd3812b69b6a38b97')
    # for x in h:
    #     print(str(x.change_type) + '|' + str(x.a_path))

    # git的index空间就是cache空间(暂存区)
    # index = repo.index
    # print(dir(index))
    # compress_file_handle("../../test/frp_0.26.0_linux_amd64.tar.gz", "../../test/test1/")
    # compress_file_handle("../../test/django_git.zip", "../../test/test1")
    compress_file_handle("../../test/test1/urls.py", "../../test/test2")