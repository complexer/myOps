import os
import zipfile
import git
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
    index.commit(message='test')