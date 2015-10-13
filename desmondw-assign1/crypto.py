"""
Assignment 1: Cryptography
Course: CS 92SI
Name: Desmond Chan 
Date: 10/8/15

This is a cryptography suite, where users can choose to encrypt or decrypt either strings or files using one of 3 methods:
1. Caesar, which shifts letters by certain number of spaces in the alphabet
2. Vigenere, which shifts letter by varying number of spaces in the alphabet according to a passkey
3. Railfence, which draws out the word in a zig-zag pattern and reads the result row by row.
"""

def encrypt_caesar(plaintext):
    """
    Encrypts plaintext using a Caesar cipher.
    First the plaintext is converted in upper case. Then according to the encryption dictionary,
    it maps each letter from the original plaintext to its encrypted letter. It then returns
    the new string.
    """
    plaintext = plaintext.upper()
    caesar_encr = {'A':'D', 'B':'E', 'C':'F', 'D':'G', 'E':'H', 'F':'I', 'G':'J', 'H':'K', 'I':'L', 'J':'M',
    'K':'N', 'L':'O', 'M':'P', 'N':'Q', 'O':'R', 'P':'S', 'Q':'T', 'R':'U', 'S':'V', 'T':'W', 'U':'X', 'V':'Y', 'W':'Z',
    'X':'A', 'Y':'B', 'Z':'C'}
    newtext = ""
    for letter in range(len(plaintext)):
        newtext += caesar_encr.get(plaintext[letter])
    return newtext

def decrypt_caesar(ciphertext):
    """
    Decrypts a ciphertext using a Caesar cipher.
    First the ciphertext is converted into upper case. Then according to the decryption dictionary,
    it maps each letter from the ciphertext to its decrypted letter. It then returns
    the decrypted string.
    """
    ciphertext = ciphertext.upper()
    caesar_decr = {'A':'X', 'B':'Y', 'C':'Z', 'D':'A', 'E':'B', 'F':'C', 'G':'D', 'H':'E', 'I':'F', 'J':'G',
    'K':'H', 'L':'I', 'M':'J', 'N':'K', 'O':'L', 'P':'M', 'Q':'N', 'R':'O', 'S':'P', 'T':'Q', 'U':'R', 'V':'S', 'W':'T',
    'X':'U', 'Y':'V', 'Z':'W'}
    newtext = ''
    for letter in range(len(ciphertext)):
        newtext += caesar_decr.get(ciphertext[letter])
    return newtext

def encrypt_vigenere(plaintext, keyword):
    """
    Encrypts plaintext using a Vigenere cipher with a keyword.
    First it multiplies the keyword so that it is the same length as the plaintext. Then it takes the 
     number of each letter the plaintext and its corresponding keyword's number. These numbers are added together,
     and the encvrypted letter is assigned according to the vigenere dictionary.
    Lastly it returns the encrypted string.
    """
    plaintext = plaintext.upper()
    keyword = keyword.upper()
    newtext = ''
    vigenere_dict = {0:'A', 1:'B', 2:'C', 3:'D', 4:'E', 5:'F', 6:'G', 7:'H', 8:'I', 9:'J', 10:'K', 11:'L', 12:'M', 13:'N', 14:'O', 15:'P', 
    16:'Q', 17:'R', 18:'S', 19:'T', 20:'U', 21:'V', 22:'W', 23:'X', 24:'Y', 25:'Z'}
    encr_word = keyword * (len(plaintext)//len(keyword) + 1)
    encr_word = encr_word[0:len(plaintext)]
    for letter in range(len(plaintext)):
        orig_num = ord(plaintext[letter]) - 65
        mod_num = ord(encr_word[letter]) - 65
        sum_num = (orig_num + mod_num) % 26
        newtext += vigenere_dict[sum_num]
    return newtext


def decrypt_vigenere(ciphertext, keyword):
    """
    Decrypts ciphertext using a Vigenere cipher with a keyword.
    First it multiplies the keyword so that it is the same length as the ciphertext. Then it takes the 
    number of each letter in the ciphertext as well as the number of its corresponding keyword letter. 
    We take the difference of the ciphertext number and the keyword number, and according to the vigenere_dict
    we are able to decrypt the ciphertext. We then return the ciphertext.
    """
    ciphertext = ciphertext.upper()
    keyword = keyword.upper()
    newtext = ''
    vigenere_dict = {0:'A', 1:'B', 2:'C', 3:'D', 4:'E', 5:'F', 6:'G', 7:'H', 8:'I', 9:'J', 10:'K', 11:'L', 12:'M', 13:'N', 14:'O', 15:'P', 
    16:'Q', 17:'R', 18:'S', 19:'T', 20:'U', 21:'V', 22:'W', 23:'X', 24:'Y', 25:'Z'}
    encr_word = keyword * (len(ciphertext)//len(keyword) + 1)
    encr_word = encr_word[0:len(ciphertext)]
    for letter in range(len(ciphertext)):
        orig_num = ord(ciphertext[letter]) - 65
        mod_num = ord(encr_word[letter]) - 65
        diff_num = (orig_num - mod_num) % 26
        newtext += vigenere_dict[diff_num]
    return newtext


def encrypt_railfence(plaintext, num_rails):
    """
    Encrypts plaintext using a railfence cipher.
    This follows a pattern that's found in the railfence, where in the first and last rows
    the gaps between each letter are equal. In all other rows, you can see it as two different
    starting points, but with the same gap amount. Therefore the rows in between the first and last
    row are made up of two lists which are then combined together. The gap between letters is calculated
    as the number of rails multiplied by 2 minus 2. 
    """
    gap = num_rails * 2 - 2
    newtext = ''
    for i in range(num_rails):
        if i == 0:
            newtext += plaintext[::gap]
        elif i == num_rails - 1 and i < len(plaintext):
            newtext += plaintext[num_rails - 1::gap]
        else:
            if i < len(plaintext): 
                vec1 = plaintext[i::gap]
                vec2 = plaintext[gap-i::gap]
                comb_vec = ''
                for i in range(len(vec2)):
                    newtext += vec1[i]
                    newtext += vec2[i]
                if len(vec1) > len(vec2):   #This is the case when vector 1 is longer than vector 2
                    newtext += vec1[len(vec1) - 1]  #Vector 2 will never be longer than vector 1
    return newtext

def decrypt_railfence(ciphertext, num_rails):
    """
    Decrypts ciphertext using a railfence cipher.
    Unfinished....
    """
    gap = num_rails * 2 - 2
    newtext = ''
    lengths = []
    groups = []
    for i in range(gap):
        if i < len(ciphertext):
            lengths[i] = (len(ciphertext)  - i)/ gap + 1

    for i in range(num_rails):
        if i == 0:
            groups[i] = lengths[0]
        elif i == num_rails - 1:
            if i < len(ciphertext):
                groups[i] = lengths[num_rails - 1]
        else:
            if i < len(ciphertext):
                groups[i] = lengths[i] + lengths[gap - i]

    return newtext


def read_from_file(filename):
    """
    Reads and returns content from a file.
    It uses file I/O to read a file with read-only permission. 
    It then returns the content found in the file.
    """
    with open(filename, 'r') as f:
        content = f.read()
    return content



def write_to_file(filename, content):
    """
    Writes content to a file.
    It uses file I/O to write the transformed text into the specified file.
    """
    with open(filename, 'w') as f:
        f.write(content)


def run_suite():
    """
    Runs a single iteration of the cryptography suite.

    Asks the user for input text from a string or file, whether to encrypt
    or decrypt, what tool to use, and where to show the output.
    """
    print("*Input*")
    filetype = input('(F)ile or (S)tring? ')
    original = ''
    if filetype == 'F' or filetype == 'f':
        filename = input('Enter the file to encrypt or decrypt: ')
        original = read_from_file(filename)
        original = original.replace(" ", "")
    if filetype == 'S' or filetype == 's':
        string = input('Enter the string to encrypt or decrypt: ')
        original = string
        original = original.replace(" ", "")

    print("*Transform*")
    mode = input('(E)ncrypt or (D)ecrypt? ')
    method = input('(C)aesar, (V)igenere, or (R)ailfence? ')
    transformed = ''
    if mode == 'e' or mode == 'E':
        if method == 'v' or method == 'V':
            passkey = input('Passkey? ')
            transformed = encrypt_vigenere(original, passkey)
        elif method == 'R' or method == 'r':
            rails = input('Number of rails? ')
            rails = int(rails)
            transformed = encrypt_railfence(original, rails)
        elif method == 'C' or method == 'c':
            transformed = encrypt_caesar(original)

    elif mode == 'D' or mode == 'd':
        if method == 'v' or method == 'V':
            passkey = input('Passkey? ')
            transformed = decrypt_vigenere(original, passkey)
        elif method == 'R' or method == 'r':
            rails = input('Number of rails? ')
            rails = int(rails)
            transformed = decrypt_railfence(original, rails)
        elif method == 'C' or method == 'c':
            transformed = decrypt_caesar(original)     


    print("*Output*")
    outputtype = input('(F)ile or (S)tring? ')
    outputname = ''
    if outputtype == 'F' or outputtype == 'f':
        outputname = input('Filename? ')
        write_to_file(outputname, transformed)
        print('Transformed text written to ' + outputname)
    if outputtype == 'S' or outputtype == 's':
        print('The transformed text is:' + transformed)


# Do not modify code beneath this point.
def should_continue():
    """
    Asks the user whether they would like to continue.
    Responses that begin with a `Y` return True. (case-insensitively)
    Responses that begin with a `N` return False. (case-insensitively)
    All other responses (including '') cause a reprompt.
    """
    choice = input("Again (Y/N)? ").upper()
    while not choice or choice[0] not in ['Y', 'N']:
        choice = input("Please enter either 'Y' or 'N'. Again (Y/N)? ").upper()
    return choice[0] == 'Y'


def main():
    """Harness for the Cryptography Suite"""
    print("Welcome to the Cryptography Suite!")
    run_suite()
    while should_continue():
        run_suite()
    print("Goodbye!")


if __name__ == '__main__':
    """This block is run if and only if the Python script is invoked from the
    command line."""
    main()
