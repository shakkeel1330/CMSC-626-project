import string

shared_ref_map_dir = "C:\\Users\\jeffe\\Projects\\test-dir"
path_ref="\\"
last_path_ref_index = shared_ref_map_dir[::-1].index(path_ref)
#print(last_path_ref_index)
#print("Word is "+shared_ref_map_dir[len(shared_ref_map_dir)-last_path_ref_index:])
#print(shared_ref_map_dir[:len(shared_ref_map_dir)-last_path_ref_index])

def caesar(text, step):
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

#print(getcipheredaddress(shared_ref_map_dir))

#print(getdecipheredaddress(getcipheredaddress(shared_ref_map_dir)))
perm_home = "C:\\Users\\jeffe\\Projects\\test-dir"
len_ph = len(perm_home)
substr = 'C:\\Users\\jeffe\\Projects\\test-dir\\def\\def'
final_str=""
for sub_str in substr[len_ph+1:].split("\\"):
    final_str = final_str +"\\"+ caesar(sub_str,-3)
print(perm_home+final_str)