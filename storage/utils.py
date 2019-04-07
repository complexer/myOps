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
    res = index.commit(message='test')
    return res


class RepoHandle(object):

    def __init__(self, path):
        self.repo = git.Repo(path)
        self.git = self.repo.git
        self.head_commit = self.repo.head.commit

    def repo_search(self, file_hexsha):
        file_type = self.git.cat_file('-t', file_hexsha)
        file_content = self.git.cat_file('-p', file_hexsha)
        if file_type == "tree":
            print(file_type)
            file_lists = []
            for file_list in file_content.replace("\t", " ").split("\n"):
                file_dic = {}
                file_info = file_list.split(" ")
                print(file_info)
                file_dic['mode'] = file_info[0]
                file_dic['type'] = file_info[1]
                file_dic['hexsha'] = file_info[2]
                file_dic['name'] = file_info[3]
                file_lists.append(file_dic)
            return file_lists, file_type
        elif file_type == "blob":
            print(file_type)
            return file_content, file_type

    def get_repo_last_commit(self):
        last_commits = list(self.repo.iter_commits('master', max_count=20))
        # for c in last_commits:
        #     commit_hexsha = c.hexsha
        #     commit_tree_hexsha = c.tree.hexsha
        return last_commits

if __name__ == '__main__':
    repo_handle = RepoHandle('../repository/test')

    # repo_handle.get_repo_last_commit()
    file_content, file_type = repo_handle.repo_search("c0b59a1c16230514dcb196010884174b3cb25923")


