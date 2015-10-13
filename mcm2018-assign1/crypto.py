"""
File: crypto.py
Name: Matt Mahowald
Date: October 9th 2015
Description: crypto.py implements a cryptography suite that allows
the user to input a message or a filename and then either encrypt 
or decrypt the message
"""
# Import to check if a file exists
import os.path

NUM_ALPHA_LETTERS = 26
CAESAR_OFFSET = 3

def format_text(text):
    # Formats all text to upper case and only alpha characters
    to_encrypt = ""
    for ch in text:
        if(ch.isalpha()):
            to_encrypt += ch
    return to_encrypt.upper()

def encrypt_caesar(plaintext):
    """
    Encrypts plaintext using a Caesar cipher.
    Creates a string to which each character offset by CAESAR_OFFSET
    is appended, unless the character's ASCII value + CAESAR_OFFSET
    is greater thah the ASCII value of 'Z', in which case the func
    subtracts by NUM_ALPHA_LETTERS
    """
    plaintext = format_text(plaintext)
    print("Encrypting {0} using Caesar cipher".format(plaintext))
    new_string = ""
    for letter in plaintext:
        if(letter.isalpha()):
            if((ord(letter) + CAESAR_OFFSET) <= ord('Z')):
                new_string += chr((ord(letter) + CAESAR_OFFSET))
            else:
                new_string += chr((ord(letter) + CAESAR_OFFSET - NUM_ALPHA_LETTERS))
    return new_string

def decrypt_caesar(ciphertext):
    """
    Decrypts a ciphertext using a Caesar cipher.
    Reverses the operation of the Caesar encryption, subtracting 
    CAESAR_OFFSET from each character, wrapping around the end of
    the alphabet.
    """
    ciphertext = format_text(ciphertext)
    print("Decrypting {0} using Caesar cipher".format(ciphertext))
    new_string = ""
    for letter in ciphertext:
        if(letter.isalpha()):
            if((ord(letter) - CAESAR_OFFSET) >= ord('A')):
                new_string += chr((ord(letter) - CAESAR_OFFSET))
            else:
                new_string += chr((ord(letter) - CAESAR_OFFSET + NUM_ALPHA_LETTERS))
    return new_string

def encrypt_vigenere(plaintext, keyword):
    """
    Encrypts plaintext using a Vigenere cipher with a keyword.
    Accepts a keyword to align with the text to be encoded, adding the
    distance between 'A' and each letter of the keyword to each character's
    ASCII value.
    """
    plaintext = format_text(plaintext)
    keyword = format_text(keyword)
    if(keyword == ""): return plaintext
    print("Encrypting {0} using Vigenere cipher with key {1}".format(plaintext, keyword))
    plaintext = plaintext.upper()
    new_string = ""
    for i in range(len(plaintext)):
        key_char = keyword[i % len(keyword)]
        new_chr = chr(ord(plaintext[i]) + ord(key_char) - ord('A'))
        while(ord(new_chr) < ord('A') or ord(new_chr) > ord('Z')):
            new_chr = chr(ord(new_chr) - NUM_ALPHA_LETTERS)
        new_string += new_chr
    return new_string

def decrypt_vigenere(ciphertext, keyword):
    """
    Decrypts ciphertext using a Vigenere cipher with a keyword.
    Accepts a keyword to align with the text to be decoded, subtracting the
    distance between 'A' and each letter of the keyword to each character's
    ASCII value.
    """
    keyword = format_text(keyword)
    ciphertext = format_text(ciphertext)
    if(keyword == ""): return ciphertext
    print("Decrypting {0} using Vigenere cipher with key {1}".format(ciphertext, keyword))
    new_string = ""
    for i in range(len(ciphertext)):
        key_char = keyword[i % len(keyword)]
        new_chr = chr(ord(ciphertext[i]) + ord('A') - ord(key_char))
        if(not new_chr.isalpha()):
            new_chr = chr(ord(new_chr) + NUM_ALPHA_LETTERS)
        new_string += new_chr
    return new_string
    
def encrypt_railfence(plaintext, num_rails):
    """
    Encrypts plaintext using a railfence cipher.
    Traverses the string as if it were a zig zag, adding each
    letter to its "rail", represented by a list of strings to
    designate each row of the railfence

    WEAREDISCOVEREDFLEEATONCE 
            becomes 
    W   E   C   R   L   T   E
     E R D S O E E F E A O C
      A   I   V   D   E   N
    WECRLTEERDSOEEFEAOCAIVDEN
    """
    plaintext = format_text(plaintext)
    print("Encrypting {0} using railfence cipher with {1} rails".format(plaintext, num_rails))
    rails =[""] * num_rails
    row = 0
    d_row = -1
    for ch in plaintext:
        if(not ch.isalpha()): continue
        if(row == (num_rails - 1) or row == 0):
            d_row *= -1
        rails[row] = rails[row] + ch
        row += d_row
    return "".join(rails)
    # http://codegolf.stackexchange.com/questions/10544/rail-fence-cipher



def decrypt_railfence(ciphertext, num_rails):
    """
    Decrypts ciphertext using a railfence cipher.
    Identifies the different rails, then strings them together
    one letter at a time, traversing the path of the rail.
    """
    ciphertext = format_text(ciphertext)
    print("Decrypting {0} using railfence cipher with {1} rails".format(ciphertext, num_rails))
    railfence_constant = (num_rails - 1) * 2
    l = []
    rail_length = len(ciphertext) // railfence_constant
    leftover = len(ciphertext) % railfence_constant
    letters_used = 0
    # Walks through string, breaking up the cipher into the "rails"
    for i in range(railfence_constant):
        if(leftover > 0):
            l.append(ciphertext[letters_used: letters_used + rail_length + 1])
            letters_used += rail_length + 1
            leftover -= 1
        else:
            l.append(ciphertext[letters_used: letters_used + rail_length])
            letters_used += rail_length
    secret_message = ""
    # Combines the rail pairs except for the edge case rails
    for i in range(num_rails):
        if(i == 0 or i == num_rails - 1): 
            continue
        l[i] = l[i] + l[i + 1]
        l.remove(l[i + 1])
    row = 0
    d_row = -1
    # Walks through rail position, combining rails into the secret message
    for i in ciphertext:
        if(row == (num_rails - 1) or row == 0):
            d_row *= -1
        secret_message += l[row][0]
        l[row] = l[row][1:]
        row += d_row
    return secret_message

def read_from_file(filename):
    """
    Reads and returns content from a file.
    Returns a string representation of the file, could be troublesome
    for larger files. Probably should revise to deal with this case
    entirely separatelt in the program.
    """
    raw_text = ""
    with open(filename, 'r') as f:
        lines = f.readlines()
    for line in lines:
        for ch in line:
            if(ch.isalpha()):
                raw_text += ch
    return raw_text


def write_to_file(filename, content):
    # Writes passed in content to any file, existing or not.
    print("Writing content to {0}...".format(filename))
    with open(filename, 'w+') as f:
        f.write(content)

def get_keyword():
    # Prompts for a keyword, assuring the keyword is not an empty string
    word = input("Passkey? ").upper()
    while(word == ""):
        input("Please enter any sequence of characters: ").upper()
    return word

def get_nrails():
    '''
    Prompts user for an integer, error checking to insure input is of
    the correct type.
    '''
    user_input = input("Enter an integer: ")
    try:
        val = int(user_input)
    except ValueError:
        print("That's not an int!")
    # http://stackoverflow.com/questions/5424716/python-how-to-check-if-input-is-a-number
    return val

def transform_text(raw_text, operation, tool):
    """
    Operates the requested encryption/decryption using
    the proper tool.
    """
    if(operation == 'E'):
        if  (tool == 'C'):
            return encrypt_caesar(raw_text)
        elif(tool == 'V'):
            return encrypt_vigenere(raw_text, get_keyword())
        elif(tool == 'R'):
            return encrypt_railfence(raw_text, get_nrails())
    elif(operation == 'D'):
        if  (tool == 'C'):
            return decrypt_caesar(raw_text)
        elif(tool == 'V'):
            return decrypt_vigenere(raw_text, get_keyword())
        elif(tool == 'R'):
            return decrypt_railfence(raw_text, get_nrails())
    else:
        print("We're sorry, an error has occurred")

def prompt_for_filename():
    # Assumes user will enter a valid filename
    return input('Filename? ')

def run_suite():
    """
    Runs a single iteration of the cryptography suite.

    Asks the user for input text from a string or file, whether to encrypt
    or decrypt, what tool to use, and where to show the output.
    """
    print("*Input*")
    raw_text = "" # the to-be-encrypted/decrypted text 
    if(type_is_file()):
        filename = prompt_for_filename()
        while(not os.path.exists(filename)):
            filename = prompt_for_filename()
        raw_text = read_from_file(filename).upper()
    else:
        raw_text = input("Enter the string to encrypt or decrypt: ").upper()

    print("*Transform*")
    operation = transformation_type()
    tool = encryption_method() 
    message = transform_text(raw_text, operation, tool)
    print("...")

    print("*Output*") 
    if(type_is_file()):
        write_to_file(prompt_for_filename(), message)
    else:
        print(message)

def encryption_method():
    # Requests, returns, and error checks for the method of en/decryption
    """
    Asks the user how they would like to encrypt or decrypt.
    Responses that begin with a `C` return 'C'. (case-insensitively)
    Responses that begin with a `V` return 'V'. (case-insensitively)
    Responses that begin with a `R` return 'R'. (case-insensitively)
    All other responses (including '') cause a reprompt.
    """    
    input_type = input("(C)aesar, (V)igenere, or (R)ailfence? ").upper()
    while not input_type or input_type[0] not in ['C', 'V', 'R']:
        input_type = input("Please enter either 'C', 'V', or 'R': ").upper()
    return input_type[0]  

def transformation_type():
    """
    Asks the user whether they would like to encrypt or decrypt.
    Responses that begin with a `E` return 'E'. (case-insensitively)
    Responses that begin with a `D` return 'D'. (case-insensitively)
    All other responses (including '') cause a reprompt.
    """    
    input_type = input("(E)ncrypt or (D)ecrypt? ").upper()
    while not input_type or input_type[0] not in ['E', 'D']:
        input_type = input("Please enter either 'E' or 'D': ").upper()
    return input_type[0]

def type_is_file():
    """
    Asks the user whether they would like to use a string or a file.
    Responses that begin with a `F` return True. (case-insensitively)
    Responses that begin with a `S` return False. (case-insensitively)
    All other responses (including '') cause a reprompt.
    """
    selection = input("(F)ile or (S)tring? ").upper()
    while not selection or selection[0] not in ['F', 'S']:
        selection = input("Please enter either 'F' or 'S': ").upper()
    return selection[0] == 'F'

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