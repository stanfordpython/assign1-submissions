"""
Assignment 1: Cryptography
Course: CS 92SI
Name: Keyur Mehta
Date: 10/7/2015

Replace this with a description of the program.
"""
import math

def encrypt_caesar(plaintext):
    """
    Encrypts plaintext using a Caesar cipher.
    Creates a dictionary that maps the letters to their Caesar equivalent. 
    Uses that dictionary to make ciphertext
    """

    alpha_str = "abcdefghijklmnopqrstuvwxyz"
    caesar_for_map = {letter:alpha_str[(index+3)%26] for index, letter in enumerate(alpha_str)}

    ptext = plaintext.lower()
    new_text = ''

    for letter in ptext:
        new_text = new_text + caesar_for_map.get(letter)

    return new_text


def decrypt_caesar(ciphertext):
    """
    Decrypts a ciphertext using a Caesar cipher.
    Creates a Caesar to plain dictionary by reversing the previously made one. 
    Uses this dictionary to create the plaintext. 
    """
    alpha_str = "abcdefghijklmnopqrstuvwxyz"
    caesar_for_map = {letter:alpha_str[(index+3)%26] for index, letter in enumerate(alpha_str)}
    caesar_rev_map = {value:key for key, value in caesar_for_map.items()}

    ctext = ciphertext.lower()
    new_text = ''

    for letter in ctext:
        new_text = new_text + caesar_rev_map.get(letter)

    return new_text


def encrypt_vigenere(plaintext, keyword):
    """
    Encrypts plaintext using a Vigenere cipher with a keyword.
    Gets the proper key by extending it if its too small and then selecting the letters to match the plaintext length.
    Uses the ord and chr functions to convert letters to their number equivelent add them and then convert back to letters. 
    """
    p_text = plaintext.upper()
    kw_extend = (keyword*(math.ceil(len(p_text)/len(keyword))))[:len(p_text)].upper()

    new_word = ''
    for index, letter in enumerate(p_text):
        new_word = new_word + chr(65+((ord(letter) + ord(kw_extend[index]) - 65*2) % 26))

    return new_word


def decrypt_vigenere(ciphertext, keyword):
    """
    Decrypts ciphertext using a Vigenere cipher with a keyword.
    Gets the proper key by extending it if its too small and then selecting the letters to match the ciphertext length.
    Uses the ord and chr functions to convert letters to their number equivelent subtract the keyword from the cipher to get the plain
    """
    c_text = ciphertext.upper()
    kw_extend = (keyword*(math.ceil(len(c_text)/len(keyword))))[:len(c_text)].upper()

    new_word = ''
    for index, letter in enumerate(c_text):
        new_word = new_word + chr(65+((ord(letter) - ord(kw_extend[index]) - 65*2) % 26))

    return new_word

#ERROR CHECKING WITH SHORT STRINGS
def encrypt_railfence(plaintext, num_rails):
    """
    Encrypts plaintext using a railfence cipher.
    Determines the increment depending on the number of rails. Then creates a word to add
    based on if its on the ends or in the middle, using the increment.
    """
    p_text = plaintext.upper()
    new_word = ''

    if num_rails == 1:
        increment = 1
    else:
        increment = num_rails*2 - 2

    for i in range(num_rails):
        if i == 0 or i == num_rails-1:
            new_word = new_word + p_text[i::increment]
        else:
            new_seg_1 = p_text[i::increment]
            start = 2*(num_rails - 1) - i
            new_seg_2 = p_text[start::increment]

            # word_add = ''*(len(new_seg_1) + len(new_seg_2))
            # word_add[::2] = p_text[i::increment]
            # word_add[1::2] = p_text[start::increment]

            word_add = ''
            for ind, let in enumerate(new_seg_1):
                if len(new_seg_1) != len(new_seg_2) and ind == len(new_seg_2):
                    word_add = word_add + let
                else:
                    word_add = word_add + let + new_seg_2[ind]
                    
            new_word = new_word + word_add
    return new_word


def decrypt_railfence(ciphertext, num_rails):
    """
    Encrypts plaintext using a railfence cipher.
    Creates a new vector that stores the actual indices of all the letters in the ciphertext.
    Uses these indices to rearrange the letters in the ciphertext order. 
    """
    c_text = ciphertext.upper()
    new_word_list = ['']*len(c_text)

    if num_rails == 1:
        increment = 1
    else:
        increment = num_rails*2 - 2

    ind_list = []
    
    for i in range(num_rails):
        if i == 0 or i == num_rails-1:
            new_nums = range(i, len(c_text), increment)
        else:
            new_seg_1 = range(i, len(c_text), increment)
            start = 2*(num_rails - 1) - i
            new_seg_2 = range(start, len(c_text), increment)

            new_nums = []
            for ind, num in enumerate(new_seg_1):
                if len(new_seg_1) != len(new_seg_2) and ind == len(new_seg_2):
                    new_nums.append(num)
                else:
                    new_nums.append(num)
                    new_nums.append(new_seg_2[ind])

        for n in new_nums:
            ind_list.append(n)

    for ind,num in enumerate(ind_list):
        new_word_list[num] = c_text[ind];

    new_str = ''.join(new_word_list)
    return new_str


def read_from_file(filename):
    """
    Reads and returns content from a file.
    Uses with for error catching.
    """
    with open(filename) as f:
        content = f.readlines()
    return content[0]


def write_to_file(filename, content):
    """
    Writes content to a file.
    Uses with for error checking. 
    """

    with open(filename, "wt") as f:
        f.write(content)

def mod_string(old_str):
    """
    Removes all of the non-letters from the string. 
    """
    new_str = ''
    for letter in old_str:
        if letter.isalpha():
            new_str = new_str + letter
    new_str = new_str.upper()
    return new_str

def run_suite():
    """
    Runs a single iteration of the cryptography suite.

    Asks the user for input text from a string or file, whether to encrypt
    or decrypt, what tool to use, and where to show the output.
    """
    print("*Input*")

    to_read = ''
    filename = ''
    while(True):
        inp = input("(F)ile or (S)tring? ").lower()
        if inp == 'f':
            filename = input("Filename: ")
            to_read = mod_string(read_from_file(filename))
            break
        elif inp == 's':
            to_read = mod_string(input("Enter the string to encrypt: "))
            break
   
    print("*Transform*")

    en_or_de = ''
    while(True):
        en_or_de = input("(E)ncrypt or (D)ecrypt? ").lower()
        if en_or_de == 'e' or en_or_de == 'd':
            break

    cryp_type = ''
    while(True):
        cryp_type = input("(C)aesar, (V)igenere, or (R)ailfence? ").lower()
        if(cryp_type == 'c' or cryp_type == 'v' or cryp_type == 'r'):
            break

    type_print = ''
    if en_or_de == 'e':
        gen_type = "Encrypting"
        if cryp_type == 'c':
            crpy_out = encrypt_caesar(to_read)
            type_print = "Caesar"
            extra = ""
        elif cryp_type == 'v':
            passkey = mod_string(input("Passkey? "))
            crpy_out = encrypt_vigenere(to_read, passkey)
            type_print = "Vigenere"
            extra = "with key " + passkey 
        else:
            num_rails = int(input("Number of rails? "))
            crpy_out = encrypt_railfence(to_read, num_rails)
            type_print = "Railfence"
            extra = "with " + str(num_rails) + " rails."
    else:
        gen_type = "Decrypting"

        if cryp_type == 'c':
            crpy_out = decrypt_caesar(to_read)
            type_print = "Caesar"
            extra = ""
        elif cryp_type == 'v':
            passkey = input("Passkey? ")
            crpy_out = decrypt_vigenere(to_read, passkey)
            type_print = "Vigenere"
            extra = "with key " + passkey
        else:
            num_rails = int(input("Number of rails? "))
            crpy_out = decrypt_railfence(to_read, num_rails)
            type_print = "Railfence"
            extra = "with " + str(num_rails) + " rails."

    if inp == 'f':
        print(gen_type, "contents of", filename, "using", type_print, "cipher", extra)
    else:
        print(gen_type, to_read, "using", type_print, "cipher", extra)

    print("*Output*")

    while(True):
        out_type = input("(F)ile or (S)tring? ")
        type_out = "plaintext"
        if en_or_de == 'e':
            type_out = "ciphertext"
        if out_type == 'f':
            out_file = input("Filename: ")
            to_read = write_to_file(out_file, crpy_out)
            print("Writing ", type_out, " to ", out_file)
            break
        elif out_type == 's':
            print("The ", type_out, "is: ", crpy_out)
            break

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
