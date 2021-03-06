#
from .utils import *
from .forms import *
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect,HttpResponse


shared_ref_map = {}
shared_ref_dir = 'F:\\project\\DAlphaFS'
path_ref = '\\'
perm_home= shared_ref_dir

def gotoHomePage(request):
    global shared_ref_dir
    global shared_ref_map
    global perm_home
    shared_ref_map_dir = shared_ref_map[str(request.user)]
    dirs,files,file_status_corrupt = get_content(shared_ref_map_dir,True,True,str(request.user))
    shared_ref_map_dir = shared_ref_map[str(request.user)]
    curr_dir = getdecipheredcurraddress(shared_ref_map_dir,perm_home)
    #print("Current directory is"+curr_dir)
    filesafe = True
    
    if(not file_status_corrupt):
        filesafe=False
    shared_ref_map[str(request.user)] = shared_ref_map_dir
    return render(request, template_name='shared_dir.html',
                  context = {'dirs': dirs, 'files': files,'curr_dir' :curr_dir,'filesafe':filesafe})

@login_required(login_url='login')
def shared_dir(request):
    print(get_client_ip(request))
    global shared_ref_dir
    global shared_ref_map
    global perm_home
    #shared_ref_dir = 'C:\\Users\\shakk\\Desktop\\test_dir'
    #shared_ref_dir = 'C:\\Users\\jeffe\\Projects\\test-dir'
    
    shared_ref_map[str(request.user)] = perm_home
    shared_ref_map_dir = shared_ref_map[str(request.user)]
    #original_dir = shared_ref_map_dir
    curr_dir = getdecipheredcurraddress(shared_ref_map_dir,perm_home)
    dirs,files,file_status_corrupt = get_content(shared_ref_map_dir,True,True,str(request.user))
    print("file_status_corrupt"+str(file_status_corrupt))
    shared_ref_map[str(request.user)] = shared_ref_map_dir
    filesafe = True
    if(not file_status_corrupt):
        filesafe=False
    return render(request, template_name='shared_dir.html',
                  context = {'dirs': dirs, 'files': files,'curr_dir' :curr_dir,'filesafe':filesafe})

@login_required(login_url='login')
def dir_traversal(request,dir):
    global shared_ref_dir
    global shared_ref_map
    global perm_home
    #shared_ref_dir = shared_ref_dir + path_ref + dir
    #original_dir = shared_ref_map_dir
    file_status_corrupt = True
    shared_ref_map_dir = shared_ref_map[str(request.user)] + path_ref + caesar(dir,3)
    #curr_dir = shared_ref_map[str(request.user)] + path_ref + dir
    curr_dir = getdecipheredcurraddress(shared_ref_map_dir,perm_home)
    shared_ref_map[str(request.user)] = shared_ref_map_dir
    print("Directory to traverse is"+dir+"shared path is"+shared_ref_map_dir)
    dirs,files,file_status_corrupt = get_content(shared_ref_map_dir,True,True,str(request.user))
    #curr_dir = shared_ref_dir
    filesafe = True
    if(not file_status_corrupt):
        filesafe=False
    shared_ref_map[str(request.user)] = shared_ref_map_dir
    return render(request, template_name='shared_dir.html',
                  context = {'dirs': dirs, 'files': files,'curr_dir' :curr_dir,'filesafe':filesafe})

@login_required(login_url='login') 
def deleteFile(request,file_name):
    global shared_ref_dir
    global shared_ref_map
    global perm_home
    shared_ref_map_dir = shared_ref_map[str(request.user)]
    file_name = caesar(file_name,3)
    #file_ref_dir = shared_ref_dir + path_ref + file_name
    file_ref_dir = shared_ref_map_dir + path_ref + file_name
    util_delete_file(file_ref_dir)
    curr_dir = getdecipheredcurraddress(shared_ref_map_dir,perm_home)
    dirs,files,file_status_corrupt = get_content(shared_ref_map_dir,True,True,str(request.user))
    shared_ref_map[str(request.user)] = shared_ref_map_dir
    filesafe = True
    if(not file_status_corrupt):
        filesafe=False
    upload_uploadHistory("DELETE",str(request.user),file_ref_dir,datetime.today().strftime('%Y-%m-%d-%H:%M:%S'))
    return render(request, template_name='shared_dir.html',
                  context = {'dirs': dirs, 'files': files,'curr_dir' :curr_dir,'filesafe':filesafe})

@login_required(login_url='login')
def uploadFiletoDir(request):
    global shared_ref_dir
    global shared_ref_map
    form = UploadFileForm(request.POST, request.FILES)
    shared_ref_map_dir = shared_ref_map[str(request.user)]
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            print("Selected option is"+form.data['access_level'])
            access_level = 'Public'
            if(form.data['access_level']=='2'):
                access_level = 'Private'
            #print("Upload user" +str(request.user))
            handle_uploaded_file(request.FILES['file'], '{}{}'.format(shared_ref_map_dir+path_ref, request.FILES['file'].name),access_level,str(request.user))
            shared_ref_map[str(request.user)] = shared_ref_map_dir
            return gotoHomePage(request)
        
    shared_ref_map[str(request.user)] = shared_ref_map_dir
    return render(request,'upload.html',{'form':form})   

@login_required(login_url='login')
def download(request,file_to_download):
    global shared_ref_dir
    global shared_ref_map
    shared_ref_map_dir = shared_ref_map[str(request.user)]
    file_address = shared_ref_map_dir + path_ref + file_to_download
    shared_ref_map[str(request.user)] = shared_ref_map_dir
    return send_file(file_address,str(request.user))    

@login_required(login_url='login')
def deleteFolder(request,folder_name):
    global shared_ref_dir
    global shared_ref_map
    shared_ref_map_dir = shared_ref_map[str(request.user)]
    dir_ref_dir = shared_ref_map_dir + path_ref + caesar(folder_name, 3)
    print("lol", folder_name)
    util_delete_Folder(dir_ref_dir)
    shared_ref_map[str(request.user)] = shared_ref_map_dir
    return gotoHomePage(request)

def readFile(request,file_name):
    global shared_ref_dir
    global shared_ref_map
    shared_ref_map_dir = shared_ref_map[str(request.user)]
    path_ref ="\\"
    try:
        if request.method=="POST":
            form = readFileForm(request.POST)
            if form.is_valid():
                content = form.data['content']
                handle_save_file(content,shared_ref_map_dir+path_ref+file_name,str(request.user))
                shared_ref_map[str(request.user)] = shared_ref_map_dir
                form.clean()
                return goBack(request)
        else:

            lines = ""
            handle_read_file(shared_ref_map_dir+path_ref+file_name,str(request.user))
            print("METHOD IS"+request.method)
            with open('readme_read.txt') as f:
                lines = f.read()   
        #form.data['content'] = lines
            form = readFileForm(initial={'content':lines})
            form.data['content'] = lines
        #form = readFileForm
            shared_ref_map[str(request.user)] = shared_ref_map_dir
            
        #form.clean()
        lines=""
        with open('readme_read.txt') as f:
            lines = f.read()
        print("Lines in else"+lines)
        form = readFileForm(initial={'content': lines})
            #form.data['content'] = lines
        shared_ref_map[str(request.user)] = shared_ref_map_dir 
        return render(request,'readFile.html',{'form':form}) 
        #upload_uploadHistory("READ",str(request.user),shared_ref_map_dir+path_ref+file_name,datetime.today().strftime('%Y-%m-%d-%H:%M:%S'))
        #upload_uploadHistory("READ",user_name,address,datetime.today().strftime('%Y-%m-%d-%H:%M:%S'))
        #return render(request,'readFile.html',{'form':form}) 
    except(Exception) as error:
        print("Exception while reading the file and the exception is"+str(error))

@login_required(login_url='login')
def editFile(request,file_name):
    global shared_ref_dir
    global shared_ref_map
    shared_ref_map_dir = shared_ref_map[str(request.user)]
    path_ref ="\\"
    try:
        if(request.method=="POST"):
            form = editFileForm(request.POST)
            if form.is_valid():
                content = form.data['content']
                handle_save_file(content,shared_ref_map_dir+path_ref+file_name,str(request.user))
                shared_ref_map[str(request.user)] = shared_ref_map_dir
                form.clean()
                return gotoHomePage(request)   
            else:
                handle_edit_file(shared_ref_map_dir+path_ref+file_name,str(request.user))
                form = editFileForm()
                shared_ref_map[str(request.user)] = shared_ref_map_dir   
                lines=""
                with open('readme.txt') as f:
                    lines = f.read()
                print("Lines in else-1"+lines)
                form.data['content'] = lines
                return render(request,'editFile.html',{'form':form}) 
        else:
            handle_edit_file(shared_ref_map_dir+path_ref+file_name,str(request.user))
            
            lines=""
            with open('readme.txt') as f:
                lines = f.read()
            print("Lines in else"+lines)
            form = editFileForm(initial={'content': lines})
            #form.data['content'] = lines
            shared_ref_map[str(request.user)] = shared_ref_map_dir 
             
            return render(request,'editFile.html',{'form':form}) 
    except(Exception) as error:
        print("Exception while editing file is"+str(error))
    

    
@login_required(login_url='login')
def createFile(request):
    global shared_ref_dir
    global shared_ref_map
    shared_ref_map_dir = shared_ref_map[str(request.user)]
    path_ref ="\\"
    #print("Pre forms call")
    #file_value('tempting')
    try:
        if (request.method =="POST"):
            print("POST METHOD INVOKED")
            form = MakeFileForm(request.POST)
            if form.is_valid():
                user_name = str(request.user)
                access_level = 'Public'
                if(form.data['access_level'] == '2'):
                    access_level = 'Private'
                print("Pre create file")
                handle_make_file('{}{}'.format(shared_ref_map_dir+path_ref, form.data['name']), form.data['content'],user_name,access_level)
                print("Post create file")
                encryptFile(getcipheredaddress(str(shared_ref_map_dir)+str(path_ref)+str(form.data['name']))) 
                # Creating file/dir with same name will add _d
                #encryptFile(address)
                print("Post Encrypt file")
                shared_ref_map[str(request.user)] = shared_ref_map_dir
                return gotoHomePage(request)
            else:
                form = MakeFileForm() 
                shared_ref_map[str(request.user)] = shared_ref_map_dir   
                return render(request,'make_file.html',{'form':form})
        else:
            form = MakeFileForm()
            
            shared_ref_map[str(request.user)] = shared_ref_map_dir
            return render(request,'make_file.html',{'form':form})
    except Exception as e:
        print(e)

@login_required(login_url='login')
def make_dir(request):
    global shared_ref_dir
    global shared_ref_map
    shared_ref_map_dir = shared_ref_map[str(request.user)]
    form = MakeDirForm(request.POST)
    if request.method == 'POST':
        form = MakeDirForm(request.POST)
        if form.is_valid():
            user_name = str(request.user)
            access_level = 'Public'
            if(form.data['access_level'] == '2'):
                access_level='Private'
            handle_make_dir('{}{}'.format(shared_ref_map_dir+path_ref, form.data['name']),user_name,access_level)
            shared_ref_map[str(request.user)] = shared_ref_map_dir
            return gotoHomePage(request)
    shared_ref_map[str(request.user)] = shared_ref_map_dir
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
    global shared_ref_map
    shared_ref_map_dir = shared_ref_map[str(request.user)]
    form = ModifyPermissionForm(request.POST)
    file_path = shared_ref_map_dir + path_ref + file_name
    if request.method == 'POST':
        form = ModifyPermissionForm(request.POST)
        if form.is_valid():
            user_name = str(request.user)
            access_level = 'Public'
            if(form.data['access_level'] == '2'):
                access_level = 'Private'
            modifyPermissionindB(getcipheredaddress(file_path),access_level)
            shared_ref_map[str(request.user)] = shared_ref_map_dir
            return gotoHomePage(request)
    shared_ref_map[str(request.user)] = shared_ref_map_dir
    return render(request,'modifyPermission.html',{'form':form,'file_path':file_path})


def renameOperation(request,file_or_dir_name):
    global shared_ref_dir
    global shared_ref_map
    global perm_home
    shared_ref_map_dir = shared_ref_map[str(request.user)]
    form = renameForm(request.POST)
    curr_dir = getdecipheredcurraddress(shared_ref_map_dir,perm_home)
    file_path = shared_ref_map_dir + path_ref + file_or_dir_name
    if request.method =='POST':
        form = renameForm(request.POST)
        if form.is_valid():
            new_file_name = form.data['new_name']
            new_file_path = shared_ref_map_dir + path_ref + new_file_name
            renamefunc(file_path,new_file_path)
            shared_ref_map[str(request.user)] = shared_ref_map_dir
            return gotoHomePage(request)
    shared_ref_map[str(request.user)] = shared_ref_map_dir
    return render(request,'renameFile.html',{'form':form,'file_path':file_path})

def clickhomebtn(request):
    return HttpResponseRedirect(reverse('shared_dir'))
    #return HttpResponseRedirect('/home/')
    #return HttpResponse("abc")

@login_required(login_url='login')
def goBack(request):
    global shared_ref_dir
    global shared_ref_map
    global perm_home
    shared_ref_map_dir = shared_ref_map[str(request.user)]
    filesafe = True
    if(shared_ref_map_dir == perm_home):
        return HttpResponseRedirect(reverse('shared_dir'))
    else:
        last_path_ref_index = shared_ref_map_dir[::-1].index(path_ref)
        #print("last_path_ref_index"+str(last_path_ref_index))
        #print("shared_ref_dir"+shared_ref_dir)
        
        prev_dir = shared_ref_map_dir[:len(shared_ref_map_dir)-last_path_ref_index-1]
        print("Prev dir"+str(prev_dir))
        dirs,files,file_status_corrupt = get_content(prev_dir,True,True,str(request.user))
        if(not file_status_corrupt):
            filesafe=False
        curr_dir = getdecipheredcurraddress(prev_dir,perm_home)
        shared_ref_map_dir = prev_dir
        shared_ref_map[str(request.user)] = shared_ref_map_dir
        return render(request, template_name='shared_dir.html',
                  context = {'dirs': dirs, 'files': files,'curr_dir' :curr_dir,'filesafe':filesafe})

def getMessages(request):
    form = messageForm(request.POST)
    if(request.method == 'POST'):
        form = messageForm(request.POST)
        if form.is_valid():
            msg_key = forms.CharField(max_length=300)
            msg_key = form.data['msg_key']
            message_ls = fetchMessagesfromKey(msg_key)
            return render(request,template_name='displaymsgs.html',context ={'messages' : message_ls})
    return render(request,'getMsgKey.html',{'form':form})
