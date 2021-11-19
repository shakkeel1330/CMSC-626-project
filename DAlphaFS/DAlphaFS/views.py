#
from .utils import *
from .forms import *
from django.shortcuts import render

shared_ref_dir = 'C:\\Users\\jeffe\\Projects\\test-dir'
path_ref = '\\'

def gotoHomePage(request):
    global shared_ref_dir
    dirs,files = get_content(shared_ref_dir,True,True,True,True)
    return render(request, template_name='shared_dir.html',
                  context = {'dirs': dirs, 'files': files})

def shared_dir(request):
    print(get_client_ip(request))
    global shared_ref_dir
    shared_ref_dir = 'C:\\Users\\jeffe\\Projects\\test-dir'
    dirs,files = get_content(shared_ref_dir,True,True,True,True)
    return render(request, template_name='shared_dir.html',
                  context = {'dirs': dirs, 'files': files})

def dir_traversal(request,dir):
    global shared_ref_dir
    shared_ref_dir = shared_ref_dir + path_ref + dir
    dirs,files = get_content(shared_ref_dir,True,True,True,True)
    return render(request, template_name='shared_dir.html',
                  context = {'dirs': dirs, 'files': files})
    
def deleteFile(request,file_name):
    global shared_ref_dir
    file_ref_dir = shared_ref_dir + path_ref + file_name
    util_delete_file(file_ref_dir)
    dirs,files = get_content(shared_ref_dir,True,True,True,True)
    return render(request, template_name='shared_dir.html',
                  context = {'dirs': dirs, 'files': files})

def uploadFiletoDir(request):
    global shared_ref_dir
    form = UploadFileForm(request.POST, request.FILES)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'], '{}{}'.format(shared_ref_dir+path_ref, request.FILES['file'].name))
            return gotoHomePage(request)
    return render(request,'upload.html',{'form':form})   

def download(request,file_to_download):
    global shared_ref_dir
    file_address = shared_ref_dir + path_ref + file_to_download
    return send_file(file_address)    

def deleteFolder(request,folder_name):
    global shared_ref_dir
    dir_ref_dir = shared_ref_dir + path_ref + folder_name
    util_delete_Folder(dir_ref_dir)
    return gotoHomePage(request)

def make_dir(request):
    global shared_ref_dir
    form = MakeDirForm(request.POST)
    if request.method == 'POST':
        form = MakeDirForm(request.POST)
        if form.is_valid():
            handle_make_dir('{}{}'.format(shared_ref_dir+path_ref, form.data['name']))
            return gotoHomePage(request)
    return render(request, 'make_dir.html', {'form': form})

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip