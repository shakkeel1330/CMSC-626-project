#
from .utils import *
from .forms import *
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse

shared_ref_dir = 'C:\\Users\\jeffe\\Projects\\test-dir'
path_ref = '\\'

def gotoHomePage(request):
    global shared_ref_dir
    dirs,files = get_content(shared_ref_dir,True,True,True,True,str(request.user))
    
    return render(request, template_name='shared_dir.html',
                  context = {'dirs': dirs, 'files': files})

@login_required(login_url='login')
def shared_dir(request):
    print(get_client_ip(request))
    global shared_ref_dir
    #shared_ref_dir = 'C:\\Users\\shakk\\Desktop\\test_dir'
    shared_ref_dir = 'C:\\Users\\jeffe\\Projects\\test-dir'
    dirs,files = get_content(shared_ref_dir,True,True,True,True,str(request.user))
    return render(request, template_name='shared_dir.html',
                  context = {'dirs': dirs, 'files': files})

@login_required(login_url='login')
def dir_traversal(request,dir):
    global shared_ref_dir
    shared_ref_dir = shared_ref_dir + path_ref + dir
    dirs,files = get_content(shared_ref_dir,True,True,True,True,str(request.user))
    return render(request, template_name='shared_dir.html',
                  context = {'dirs': dirs, 'files': files})

@login_required(login_url='login') 
def deleteFile(request,file_name):
    global shared_ref_dir
    file_ref_dir = shared_ref_dir + path_ref + file_name
    util_delete_file(file_ref_dir)
    dirs,files = get_content(shared_ref_dir,True,True,True,True,str(request.user))
    return render(request, template_name='shared_dir.html',
                  context = {'dirs': dirs, 'files': files})

@login_required(login_url='login')
def uploadFiletoDir(request):
    global shared_ref_dir
    form = UploadFileForm(request.POST, request.FILES)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            print("Selected option is"+form.data['access_level'])
            access_level = 'Public'
            if(form.data['access_level']=='2'):
                access_level = 'Private'
            #print("Upload user" +str(request.user))
            handle_uploaded_file(request.FILES['file'], '{}{}'.format(shared_ref_dir+path_ref, request.FILES['file'].name),access_level,str(request.user))
            return gotoHomePage(request)
        

    return render(request,'upload.html',{'form':form})   

@login_required(login_url='login')
def download(request,file_to_download):
    global shared_ref_dir
    file_address = shared_ref_dir + path_ref + file_to_download
    return send_file(file_address)    

@login_required(login_url='login')
def deleteFolder(request,folder_name):
    global shared_ref_dir
    dir_ref_dir = shared_ref_dir + path_ref + folder_name
    util_delete_Folder(dir_ref_dir)
    return gotoHomePage(request)

@login_required(login_url='login')
def createFile(request):
    global shared_ref_dir
    try:
        if (request.method =="POST"):
            print("POST METHOD INVOKED")
            form = MakeFileForm(request.POST)
            if form.is_valid():
                user_name = str(request.user)
                access_level = 'Public'
                if(form.data['access_level'] == '2'):
                    access_level = 'Private'
                
                handle_make_file('{}{}'.format(shared_ref_dir+path_ref, form.data['name']), form.data['content'],user_name,access_level)
                encryptFile(shared_ref_dir+path_ref+form.data['name'])
                return gotoHomePage(request)
            else:
                form = MakeFileForm()    
                return render(request,'make_file.html',{'form':form})
        else:
            form = MakeFileForm()
            return render(request,'make_file.html',{'form':form})
    except Exception as e:
        print(e)

@login_required(login_url='login')
def make_dir(request):
    global shared_ref_dir
    form = MakeDirForm(request.POST)
    if request.method == 'POST':
        form = MakeDirForm(request.POST)
        if form.is_valid():
            user_name = str(request.user)
            access_level = 'Public'
            if(form.data['access_level'] == '2'):
                access_level='Private'
            handle_make_dir('{}{}'.format(shared_ref_dir+path_ref, form.data['name']),user_name,access_level)
            return gotoHomePage(request)
    return render(request, 'make_dir.html', {'form': form})

def get_client_ip(request):
    
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def modifyPermission(request,file_name):
    global shared_ref_dir
    form = ModifyPermissionForm(request.POST)
    file_path = shared_ref_dir + path_ref + file_name
    if request.method == 'POST':
        form = ModifyPermissionForm(request.POST)
        if form.is_valid():
            user_name = str(request.user)
            access_level = 'Public'
            if(form.data['access_level'] == '2'):
                access_level = 'Private'
            modifyPermissionindB(file_path,access_level)
            return gotoHomePage(request)
    return render(request,'modifyPermission.html',{'form':form,'file_path':file_path})
