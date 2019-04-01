from django.shortcuts import render
from .utils import *
from .forms import UploadFileForm


def repo_list(request):
    pass

def repo_create(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            app = request.POST.get('app')
            save_dir = handle_uploaded_file(request.FILES['file'],app)
            repo_init(save_dir)
            context = {}
            return render(request, 'storage/ok.html', context)
    else:
        forms = UploadFileForm()
        context = {}
        context['forms'] = forms
        return render(request, 'storage/upload.html', context)

def repo_show(request):
    pass

