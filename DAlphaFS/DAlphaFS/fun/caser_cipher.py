import string

def caesar(text, step):
    alphabets = (string.ascii_lowercase, string.ascii_uppercase, string.digits)
    def shift(alphabet):
        return alphabet[step:] + alphabet[:step]

    shifted_alphabets = tuple(map(shift, alphabets))
    joined_aphabets = ''.join(alphabets)
    joined_shifted_alphabets = ''.join(shifted_alphabets)
    table = str.maketrans(joined_aphabets, joined_shifted_alphabets)
    return text.translate(table)

#alphabets = (string.ascii_lowercase, string.ascii_uppercase, string.digits)
#print(caesar('Abc-xyZ.012:789?жñç', step=4, alphabets=alphabets))
dec_word=caesar('Abc', step=4)
print(caesar(dec_word,step = -4 ))