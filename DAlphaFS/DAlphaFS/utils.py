from django.http import HttpResponse
from os.path import isfile, getsize
from os import listdir, mkdir, system, stat,remove,rename
from wsgiref.util import FileWrapper
import tempfile
import shutil
from cryptography.fernet import Fernet
import psycopg2 as pgad
from datetime import datetime
import string
from .forms import *
from shutil import copyfile

def get_content(path, s_files, s_dirs,user_name):
    path = '{}/'.format(path) if path[-1] != '/' else str(path)
    dirs = []
    files = []
    try:
        for ld in listdir(path):
            if isfile('{}{}'.format(path, ld)) and s_files:
                file_user_map,file_perm_map = getFiledetails(path[:-1]+"\\"+ld)
                #if(file_user_m)
                visibility = 0
                if(file_user_map == user_name):
                    visibility= 1
                if(file_user_map == user_name or file_perm_map=='Public'):
                    files.append({'name': reverse_caesar(ld,3), 'size': stat("{}{}".format(path, ld)).st_size,'del_visibility':visibility})
            elif s_dirs:
                file_user_map,file_perm_map = getFiledetails(path[:-1]+"\\"+ld) 
                visibility =0
                if(file_user_map == user_name):
                    visibility=1
                if(file_user_map == user_name or file_perm_map=='Public'):
                    dirs.append({'name':reverse_caesar(ld,3),'del_visibility':visibility})

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

def handle_save_file(content, address,user_name):
    print("Upload address is"+address)
    print("Content is"+content)
    address = getcipheredaddress(address)
    print()
    #with open(address, 'wb+') as destination:
    destination = open(address,'w')
    destination.write(content)
    destination.close()
    dst = 'C:\\Users\jeffe\\Projects\\ComputerSecurity\\CMSC-626-project\\DAlphaFS\\DAlphaFS\\readme.txt'
    copyfile(address,dst)
    encryptFile(address)  
    upload_uploadHistory("EDIT",user_name,address,datetime.today().strftime('%Y-%m-%d-%H:%M:%S'))     

def handle_uploaded_file(f, address,access_level,user_name):
    print("Upload address is"+address)
    address = getcipheredaddress(address)
    with open(address, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    if(not checkifexists_encTbl(str(address),'permission')):

        writePermission(address,user_name,access_level,'File')
    
    encryptFile(address)  
    upload_uploadHistory("UPLOAD",user_name,address,datetime.today().strftime('%Y-%m-%d-%H:%M:%S'))     

# Check if file already exists. If yes, creates an entry in the uploadTable
def fileversionupdate(file_path,updated_user):
    try:
        conn = pgad.connect("dbname =testDB user=postgres password=Nov@2021;;")
        cur = conn.cursor()
        sql="SELECT "
    
    except(Exception) as error:
        print(error)

# For downloading file.
def send_file(address,user_name):
    original_address = address
    address = getcipheredaddress(address)
    filename = address
    fernet = Fernet(getKeyusingfileName(address).encode())
    with open(address, 'rb') as enc_file:
        encrypted = enc_file.read()
# decrypting the file
    decrypted = fernet.decrypt(encrypted)
# opening the file in write mode and
# writing the decrypted data
    with open(address, 'wb') as dec_file:
        print("Decrypted value is"+str(decrypted))
        dec_file.write(decrypted)
    wrapper = FileWrapper(open(filename, 'rb'))
    response = HttpResponse(wrapper, content_type='application/force-download')
    print("Address is"+address)
    response['Content-Disposition'] = 'attachment; filename={}'.format(original_address.split('\\')[-1].replace(' ', '-'))
    response['Content-Length'] = getsize(filename)
    encryptFileusingKey(filename,getKeyusingfileName(address).encode())
    upload_uploadHistory("DOWNLOAD",user_name,address,datetime.today().strftime('%Y-%m-%d-%H:%M:%S'))
    return response

def util_delete_Folder(folder_ref_path):
    try:
        shutil.rmtree(folder_ref_path) 
        deletefilePermission(folder_ref_path)
    except:
        pass     

def handle_make_dir(address,user_name,access_level):
    try:
        ciphered_address = getcipheredaddress(address)
        if(not checkifexists_encTbl(str(ciphered_address),'permission')):
            mkdir(ciphered_address)
            writePermission(ciphered_address,user_name,access_level,'Directory')
        else:
            while(checkifexists_encTbl(str(ciphered_address),'permission')):
                ciphered_address=ciphered_address+"_d"
            #address = address + "_d"
            mkdir(ciphered_address)
            writePermission(ciphered_address,user_name,access_level,'Directory')
        upload_uploadHistory("CREATE",user_name,ciphered_address,datetime.today().strftime('%Y-%m-%d-%H:%M:%S'))
    except:
        pass

def encryptFile(filepath):
    # Fetch input file and encrypt it during upload
    try:
        print("File encryption for address is"+str(filepath))
        key = Fernet.generate_key()
        fernet = Fernet(key)
        with open(filepath,'rb') as file:
            original = file.read()
        encrypted = fernet.encrypt(original)
        print("Key used for encryption is"+str(key.decode()))
        with open(filepath, 'wb') as encrypted_file:
            print("Writing encrypted file")
            encrypted_file.write(encrypted)
    #Check if value already exists
        if(not checkifexists_encTbl(str(filepath),'Encrypt')):
            sql="INSERT INTO \"public\".\"encryptionKeys\" VALUES("+"\'"+str(filepath)+"\'"+","+"\'"+key.decode()+"\'"+")"
            runQuery(sql)
        else:
            single_quote="\'"
            sql="UPDATE \"public\".\"encryptionKeys\" SET encrypt_key="+single_quote+key.decode()+single_quote+" WHERE \"encryptionKeys\".\"fileName\"="+single_quote+filepath+single_quote
            print("Update SQL is"+sql)
            runQuery(sql)
        print("File encryption completed")
    except(Exception) as error:
        print("Error while encrypting File"+str(error))

def encryptFileusingKey(filepath,key):
    fernet = Fernet(key)
    with open(filepath,'rb') as file:
        original = file.read()
    encrypted = fernet.encrypt(original)
    
    with open(filepath, 'wb') as encrypted_file:
        print("Writing encrypted file")
        encrypted_file.write(encrypted)

def checkifexists_encTbl(filepath,action):
    try:
        #print("Checking whether fileName already exists in encryption Table"+filepath)
        single_quote = "\'"
        if(action=="Encrypt"):
            select_sql = "SELECT * FROM \"public\".\"encryptionKeys\" WHERE \"encryptionKeys\".\"fileName\"="+single_quote + str(filepath) + single_quote
        else:
            select_sql = "SELECT * FROM \"public\".\"filePermission\" WHERE \"filePermission\".\"fileName\"="+single_quote + str(filepath) + single_quote
        #select_sql=""single_quote + str(filepath) + single_quote
        conn = pgad.connect("dbname =testDB user=postgres password=Nov@2021;;")
        cur = conn.cursor()
        print("Checking whether fileName already exists in encryption Table--2"+str(select_sql))
        cur.execute(select_sql)
        results = cur.fetchone()
        print(results)
        if(results is not None):
            print("Already exists")
            return True 
        return False
    except(Exception) as error:
        print("Error while checking filename exists in encryption Table is"+str(error))
        return True

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
            #print('Database connection closed.')

def getKeyusingfileName(filepath):
    try:
        conn = pgad.connect("dbname =testDB user=postgres password=Nov@2021;;")
        cur = conn.cursor()
        print(filepath)
        sql ="SELECT encrypt_key from \"public\".\"encryptionKeys\" WHERE \"fileName\"=" +"\'"+ str(filepath) +"\'"
        cur.execute(sql)
        key = cur.fetchone()
        #print(key[0])
        print("Key used for decryption"+str(key[0]))
        return key[0]
    except (Exception, pgad.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            #print('Database connection closed.')

def handle_edit_file(address,user_name):
    try:
        ciphered_address = getcipheredaddress(address)
        dst = 'C:\\Users\jeffe\\Projects\\ComputerSecurity\\CMSC-626-project\\DAlphaFS\\DAlphaFS\\readme.txt'
        print("ciphered_address is"+str(ciphered_address))
        filename = address
        fernet = Fernet(getKeyusingfileName(ciphered_address).encode())
        with open(ciphered_address, 'rb') as enc_file:
            encrypted = enc_file.read()
# decrypting the file
        decrypted = fernet.decrypt(encrypted)
# opening the file in write mode and
# writing the decrypted data
        #f_dst = open(dst,'w')
        with open(dst, 'wb') as dec_file:
            print("Decrypted value is"+str(decrypted))
            dec_file.write(decrypted)
        #destination = open(address,'w')
        #f_dst.write(decrypted)
        #copyfile(ciphered_address, dst)

    except(Exception) as error:
        print("Exception while editing the file"+str(error))

def handle_make_file(address, content,user_name,access_level):
    try:
        
        ciphered_address = getcipheredaddress(address)
        if(not checkifexists_encTbl(str(ciphered_address),'permission')):
            print("Making file")
            with open(ciphered_address, 'w+') as file:
                file.write(content)
            writePermission(ciphered_address,user_name,access_level,'File')
        else:
#            address = address + "_d"
            while(checkifexists_encTbl(str(ciphered_address),'permission')):
                ciphered_address=ciphered_address+"_d"
            with open(ciphered_address, 'w+') as file:
                file.write(content)
            writePermission(ciphered_address,user_name,access_level,'File')
        print("New address value is"+ciphered_address)
        upload_uploadHistory("CREATE",user_name,ciphered_address,datetime.today().strftime('%Y-%m-%d-%H:%M:%S'))
        return ciphered_address
        
    except(Exception) as error:
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
            #print('Database connection closed')

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
            #print('Database connection closed')

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
            #print('Database connection closed')

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
            #print('Database connection closed')

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
        old_path = getcipheredaddress(old_path)
        new_path = getcipheredaddress(new_path)
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
    fire_wall = True 
    conn = pgad.connect("dbname =testDB user=postgres password=Nov@2021;;")
    cur = conn.cursor()
    single_quote="\'"
    if(fire_wall):
        #Use parameterized Query
        #param_sql = "SELECT message from \"public\".\"msgTable\"  WHERE MESSAGE_KEY = %s" 
        
        param_sql="SELECT uh.\"file_action\",uh.\"username\",uh.\"filename\",uh.\"upload_dt\" FROM \"public\".\"filePermission\" fp inner join \"public\".\"uploadhistory\" uh on (uh.fileName=fp.\"fileName\") inner join \"public\".\"keyUser\" ku on (ku.username = fp.\"userName\") where ku.\"pvtKey\" = %s order by uh.upload_id desc"
        cur.execute(param_sql,[msg_key])
        results = cur.fetchall()
        total_msgs = []
        
        #files.append({'name': ld, 'size': stat("{}{}".format(path, ld)).st_size,'del_visibility':visibility})
        for result_msg in results:
            #total_msgs.append(result_msg[0])
            perm_home='C:\\Users\\jeffe\\Projects\\test-dir'
            decipher_addr = getdecipheredcurraddress(result_msg[2],perm_home)
            total_msgs.append({'action':result_msg[0],'username':result_msg[1],'filename':decipher_addr,'update_time':result_msg[3]})
        return total_msgs
    else:
        #conn = pgad.connect("dbname =testDB user=postgres password=Nov@2021;;")
        #cur = conn.cursor()
        #select_sql = "SELECT message from \"public\".\"msgTable\"  WHERE MESSAGE_KEY = " + "\'" + msg_key + "\'" 
        select_sql= "SELECT uh.\"file_action\",uh.\"username\",uh.\"filename\",uh.\"upload_dt\" FROM \"public\".\"filePermission\" fp inner join \"public\".\"uploadhistory\" uh on (uh.fileName=fp.\"fileName\") inner join \"public\".\"keyUser\" ku on (ku.username = fp.\"userName\") where ku.\"pvtKey\" = \'"+msg_key+single_quote+"order by uh.upload_id desc"
        print("Select sql is"+select_sql)
        cur.execute(select_sql)
        perm_home='C:\\Users\\jeffe\\Projects\\test-dir'
        conn.commit()
        total_msgs = []
        try:
            results = cur.fetchall()
            decipher_addr = getdecipheredcurraddress(result_msg[2],perm_home)
            for result_msg in results:
                total_msgs.append({'action':result_msg[0],'username':result_msg[1],'filename':decipher_addr,'update_time':result_msg[3]})
        except:
            return []
        return total_msgs

def checkifFireWallisOn():
    pass

def upload_uploadHistory(file_action,userName,fileName,upload_time):
    single_quote = "\'"
    insert_sql="INSERT INTO \"public\".\"uploadhistory\"(file_ACTION,USERNAME,FILENAME,UPLOAD_DT) VALUES("+single_quote+file_action+single_quote+","+single_quote+userName+single_quote+","+single_quote+fileName+single_quote+","+single_quote+upload_time+single_quote+")"
    try:
        conn = pgad.connect("dbname =testDB user=postgres password=Nov@2021;;")
        cur = conn.cursor()
        print("Inserting into history"+str(insert_sql))
        cur.execute(insert_sql)
        conn.commit()
    except(Exception) as error:
        print("Error while uploading upload History"+ error)

    

def caesar(text, step):
    alphabets = (string.ascii_lowercase, string.ascii_uppercase, string.digits)
    def shift(alphabet):
        return alphabet[step:] + alphabet[:step]

    shifted_alphabets = tuple(map(shift, alphabets))
    joined_aphabets = ''.join(alphabets)
    joined_shifted_alphabets = ''.join(shifted_alphabets)
    table = str.maketrans(joined_aphabets, joined_shifted_alphabets)
    return text.translate(table)

def reverse_caesar(text,step):
    step = -1 * step
    alphabets = (string.ascii_lowercase, string.ascii_uppercase, string.digits)
    def shift(alphabet):
        return alphabet[step:] + alphabet[:step]

    shifted_alphabets = tuple(map(shift, alphabets))
    joined_aphabets = ''.join(alphabets)
    joined_shifted_alphabets = ''.join(shifted_alphabets)
    table = str.maketrans(joined_aphabets, joined_shifted_alphabets)
    return text.translate(table)

def getcipheredaddress(address):
    path_ref="\\"
    last_path_ref_index = address[::-1].index(path_ref)
    text_to_be_ciphered = address[len(address)-last_path_ref_index:]
    return address[:len(address)-last_path_ref_index] + caesar(text_to_be_ciphered,3)

def getdecipheredaddress(address):
    path_ref="\\"
    last_path_ref_index = address[::-1].index(path_ref)
    text_to_be_ciphered = address[len(address)-last_path_ref_index:]
    return address[:len(address)-last_path_ref_index] + caesar(text_to_be_ciphered,-3)

def getdecipheredcurraddress(address,perm_home):
    len_ph = len(perm_home)
    final_str=""
    for sub_str in address[len_ph+1:].split("\\"):
        final_str = final_str +"\\"+ caesar(sub_str,-3)
    return (perm_home+final_str)
