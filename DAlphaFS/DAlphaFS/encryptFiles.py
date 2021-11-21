from cryptography.fernet import Fernet
import os 

home_dir = 'C:\\Users\\jeffe\\Projects\\test-dir'
key = Fernet.generate_key()
  
# string the key in a file

#def encryptFile(filename):
    
key = Fernet.generate_key()
print(key)
print(key.decode())
print(key.decode().encode())
with open('filekey.key', 'wb') as filekey:
   filekey.write(key)

# opening the key
with open('filekey.key', 'rb') as filekey:
    key = filekey.read()
  
# using the generated key
fernet = Fernet(key)
  
# opening the original file to encrypt
with open('Resume_JeffreyMatthewReginald.pdf', 'rb') as file:
    original = file.read()
      
# encrypting the file
encrypted = fernet.encrypt(original)
  
# opening the file in write mode and 
# writing the encrypted data
with open('encryptPdf.pdf', 'wb') as encrypted_file:
    encrypted_file.write(encrypted)

# using the key
fernet = Fernet(key)
  
# opening the encrypted file
with open('encryptPdf.pdf', 'rb') as enc_file:
    encrypted = enc_file.read()
  
# decrypting the file
decrypted = fernet.decrypt(encrypted)
  
# opening the file in write mode and
# writing the decrypted data
with open('origPdf.pdf', 'wb') as dec_file:
    dec_file.write(decrypted)