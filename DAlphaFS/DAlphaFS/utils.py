from django.http import HttpResponse
from os.path import isfile, getsize
from os import listdir, mkdir, system, stat,remove,rename
from wsgiref.util import FileWrapper
import tempfile
import shutil
from cryptography.fernet import Fernet
import psycopg2 as pgad


def get_content(path, s_files, s_dirs, h_files, h_dirs,user_name):
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
                    #file_path = (path+"\\"+ld).replace('\/\\','\\')
                    file_user_map,file_perm_map = getFiledetails(path[:-1]+"\\"+ld)
                    #if(file_user_m)
                    visibility = 0
                    if(file_user_map == user_name):
                        visibility= 1
                    if(file_user_map == user_name or file_perm_map=='Public'):
                        files.append({'name': ld, 'size': stat("{}{}".format(path, ld)).st_size,'del_visibility':visibility})
            elif s_dirs:
                if ld.startswith('.'):
                    if h_dirs:
                        dirs.append(ld)
                else:
                    file_user_map,file_perm_map = getFiledetails(path[:-1]+"\\"+ld) 
                    visibility =0
                    if(file_user_map == user_name):
                        visibility=1
                    if(file_user_map == user_name or file_perm_map=='Public'):
                        dirs.append({'name':ld,'del_visibility':visibility})

    except FileNotFoundError:
        dirs = FileNotFoundError
        files = FileNotFoundError
        return dirs, files

    except NotADirectoryError:
        dirs = NotADirectoryError
        files = NotADirectoryError
        return dirs, files

    return dirs, files

def util_delete_file(file_name):
    try:
        print("File to be removed is"+file_name)
        remove(file_name) 
        deletefileEntry(file_name)
        deletefilePermission(file_name)
    except:
        pass

def handle_uploaded_file(f, address,access_level,user_name):
    print("Upload address is"+address)
    
    with open(address, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    writePermission(address,user_name,access_level,'File')
    encryptFile(address)       

# Check if file already exists. If yes, creates an entry in the uploadTable
def fileversionupdate(file_path,updated_user):
    try:
        conn = pgad.connect("dbname =testDB user=postgres password=Nov@2021;;")
        cur = conn.cursor()
        sql="SELECT "
    
    except(Exception) as error:
        print(error)

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
        deletefilePermission(folder_ref_path)
    except:
        pass     

def handle_make_dir(address,user_name,access_level):
    try:
        mkdir(address)
        writePermission(address,user_name,access_level,'Directory')
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

def handle_make_file(address, content,user_name,access_level):
    try:
        print("Making file")
        with open(address, 'w+') as file:
            file.write(content)
    
        writePermission(address,user_name,access_level,'File')
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

def deletefilePermission(filepath):
    try:
        conn = pgad.connect("dbname =testDB user=postgres password=Nov@2021;;")
        cur = conn.cursor()
        print("Filename to be deleted is"+str(filepath))
        sql = "DELETE FROM \"public\".\"filePermission\" WHERE \"fileName\"=" +"\'"+ str(filepath) +"\'"
        cur.execute(sql)
        conn.commit()
    except (Exception,pgad.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed')

def writePermission(file_dir_name,user_name,access_level,type):
    try:
        conn = pgad.connect("dbname =testDB user=postgres password=Nov@2021;;")
        cur = conn.cursor()
        single_quote = "\'"
        sql="INSERT INTO \"public\".\"filePermission\" VALUES("+single_quote+file_dir_name+single_quote+","+single_quote+user_name+single_quote+","+single_quote+access_level+single_quote+","+single_quote+type+single_quote+")"
        cur.execute(sql)
        conn.commit()
    except(Exception,pgad.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed')

def getFiledetails(file_name):
    try:
        conn = pgad.connect("dbname =testDB user=postgres password=Nov@2021;;")
        cur = conn.cursor()
        #print("Filename to be checked in DB is"+str(file_name))
        sql = "SELECT *  FROM \"public\".\"filePermission\" WHERE \"fileName\"=" +"\'"+ str(file_name) +"\'"
        cur.execute(sql)
        results = cur.fetchall()
        file_user_map = ""
        file_perm_map = ""
        for row in results:
            fileName = row[0]
            file_user_map = row[1]
            file_perm_map = row[2]

        #print("File_user is" + file_user_map)
        #print("file_perm_map is" + file_perm_map)
        return file_user_map,file_perm_map
    except (Exception,pgad.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed')

def modifyPermissionindB(file_path,access_level):
    try:
        conn = pgad.connect("dbname =testDB user=postgres password=Nov@2021;;")
        cur = conn.cursor()
        sql = "UPDATE \"public\".\"filePermission\" SET \"Access\" = "+"\'"+access_level+"\'"+"WHERE \"fileName\" = "+"\'"+file_path+"\'"
        print("Update query is"+sql)    
        cur.execute(sql)
        conn.commit()
    except(Exception,pgad.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            #print('Database connection closed') 

def renamefunc(old_path,new_path):
    try:
        print("Old path is "+str(old_path))
        print("New path is "+str(new_path))
        rename(old_path,new_path)
        updatefileName(old_path,new_path)
    except(Exception) as error:
        print("Error while renaming "+ str(error))

# Invoked when there is a rename of the file or directory
def updatefileName(old_path,new_path):
    try:
        conn = pgad.connect("dbname =testDB user=postgres password=Nov@2021;;")
        cur = conn.cursor()
        update_key_tbl_sql = "UPDATE \"public\".\"encryptionKeys\" SET \"fileName\" =" + "\'" + new_path + "\'" +"WHERE \"fileName\" = "+"\'"+old_path+"\'"
        update_filePermission_sql = "UPDATE \"public\".\"filePermission\" SET \"fileName\" =" + "\'" + new_path + "\'" +"WHERE \"fileName\" = "+"\'"+old_path+"\'"
        cur.execute(update_key_tbl_sql)
        conn.commit()
        cur.execute(update_filePermission_sql)
        conn.commit()
    except(Exception) as error:
        print("Error while updating the database for rename"+error)

def fetchMessagesfromKey(msg_key):
    fire_wall = False 
    conn = pgad.connect("dbname =testDB user=postgres password=Nov@2021;;")
    cur = conn.cursor()
    if(fire_wall):
        #Use parameterized Query
        param_sql = "SELECT message from \"public\".\"msgTable\"  WHERE MESSAGE_KEY = %s" 
        cur.execute(param_sql,[msg_key])
        results = cur.fetchall()
        total_msgs = []
        for result_msg in results:
            total_msgs.append(result_msg[0])
        return total_msgs
    else:
        #conn = pgad.connect("dbname =testDB user=postgres password=Nov@2021;;")
        #cur = conn.cursor()
        select_sql = "SELECT message from \"public\".\"msgTable\"  WHERE MESSAGE_KEY = " + "\'" + msg_key + "\'" 
        print("Select sql is"+select_sql)
        cur.execute(select_sql)
        conn.commit()
        total_msgs = []
        try:
            results = cur.fetchall()
            
            for result_msg in results:
                total_msgs.append(result_msg[0])
        except:
            return []
        return total_msgs

def checkifFireWallisOn():
    pass


