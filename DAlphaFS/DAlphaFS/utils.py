from django.http import HttpResponse
from os.path import isfile, getsize
from os import listdir, mkdir, system, stat,remove
from wsgiref.util import FileWrapper
import tempfile
import shutil
from cryptography.fernet import Fernet
import psycopg2 as pgad


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
        deletefileEntry(file_name)
    except:
        pass

def handle_uploaded_file(f, address):
    print("Upload address is"+address)
    
    with open(address, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    encryptFile(address)       


# For downloading file.
def send_file(address):
    filename = address
    fernet = Fernet(getKeyusingfileName(address).encode())
    with open(address, 'rb') as enc_file:
        encrypted = enc_file.read()
# decrypting the file
    decrypted = fernet.decrypt(encrypted)
# opening the file in write mode and
# writing the decrypted data
    with open(address, 'wb') as dec_file:
        dec_file.write(decrypted)
    wrapper = FileWrapper(open(filename, 'rb'))
    response = HttpResponse(wrapper, content_type='application/force-download')
    print("Address is"+address)
    response['Content-Disposition'] = 'attachment; filename={}'.format(address.split('\\')[-1].replace(' ', '-'))
    response['Content-Length'] = getsize(filename)
    encryptFileusingKey(filename,getKeyusingfileName(address).encode())
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

def encryptFile(filepath):
    # Fetch input file and encrypt it during upload
    print("File encryption")
    key = Fernet.generate_key()
    fernet = Fernet(key)
    with open(filepath,'rb') as file:
        original = file.read()
    encrypted = fernet.encrypt(original)
    
    with open(filepath, 'wb') as encrypted_file:
        print("Writing encrypted file")
        encrypted_file.write(encrypted)
    sql="INSERT INTO \"public\".\"encryptionKeys\" VALUES("+"\'"+str(filepath)+"\'"+","+"\'"+key.decode()+"\'"+")"
    runQuery(sql)

def encryptFileusingKey(filepath,key):
    fernet = Fernet(key)
    with open(filepath,'rb') as file:
        original = file.read()
    encrypted = fernet.encrypt(original)
    
    with open(filepath, 'wb') as encrypted_file:
        print("Writing encrypted file")
        encrypted_file.write(encrypted)


def runQuery(sql):
    try:
        print('connecting db')
        conn = pgad.connect("dbname =testDB user=postgres password=Nov@2021;;")
        cur = conn.cursor()
        #print('PostgreSQL database version:')
        #print("SQL is"+sql)
        cur.execute(sql)
        conn.commit()
        # display the PostgreSQL database server version
    #db_version = cur.fetchone()
    #print(db_version)
       
	# close the communication with the PostgreSQL
        cur.close()
    except (Exception, pgad.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def getKeyusingfileName(filepath):
    try:
        conn = pgad.connect("dbname =testDB user=postgres password=Nov@2021;;")
        cur = conn.cursor()
        print(filepath)
        sql ="SELECT encrypt_key from \"public\".\"encryptionKeys\" WHERE \"fileName\"=" +"\'"+ str(filepath) +"\'"
        cur.execute(sql)
        key = cur.fetchone()
        print(key[0])
        #print("Key"+key)
        return key[0]
    except (Exception, pgad.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def handle_make_file(address, content):
    try:
        print("Making file")
        with open(address, 'w+') as file:
            file.write(content)
    except:
        pass

def deletefileEntry(filepath):
    try:
        conn = pgad.connect("dbname =testDB user=postgres password=Nov@2021;;")
        cur = conn.cursor()
        print("Filename to be deleted is"+str(filepath))
        sql = "DELETE FROM \"public\".\"encryptionKeys\" WHERE \"fileName\"=" +"\'"+ str(filepath) +"\'"
        cur.execute(sql)
        conn.commit()
    except (Exception,pgad.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed')