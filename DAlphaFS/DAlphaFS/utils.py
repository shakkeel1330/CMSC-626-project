from django.http import HttpResponse
from os.path import isfile, getsize
from os import listdir, mkdir, system, stat,remove
from wsgiref.util import FileWrapper
import tempfile
import shutil



def get_content(path, s_files, s_dirs, h_files, h_dirs):
    path = '{}/'.format(path) if path[-1] != '/' else str(path)
    dirs = []
    files = []
    try:
        for ld in listdir(path):
            if isfile('{}{}'.format(path, ld)) and s_files:
                if ld.startswith('.'):
                    if h_files:
                        files.append({'name': ld, 'size': stat("{}{}".format(path, ld)).st_size})
                else:
                    files.append({'name': ld, 'size': stat("{}{}".format(path, ld)).st_size})
            elif s_dirs:
                if ld.startswith('.'):
                    if h_dirs:
                        dirs.append(ld)
                else:
                    dirs.append(ld)

    except FileNotFoundError:
        dirs = FileNotFoundError
        files = FileNotFoundError
        return dirs, files

    except NotADirectoryError:
        dirs = NotADirectoryError
        files = NotADirectoryError
        return dirs, files

    return sorted(dirs), files

def util_delete_file(file_name):
    try:
        print("File to be removed is"+file_name)
        remove(file_name) 
    except:
        pass

def handle_uploaded_file(f, address):
    print("Upload address is"+address)
    with open(address, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)     

# For downloading file.
def send_file(address):
    filename = address
    wrapper = FileWrapper(open(filename, 'rb'))
    response = HttpResponse(wrapper, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename={}'.format(address.split('/')[-1].replace(' ', '-'))
    response['Content-Length'] = getsize(filename)
    return response

def util_delete_Folder(folder_ref_path):
    try:
        shutil.rmtree(folder_ref_path) 
    except:
        pass     

def handle_make_dir(address):
    try:
        mkdir(address)
    except:
        pass