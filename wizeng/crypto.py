"""
Assignment 1: Cryptography
Course: CS 92SI
Name: William Zeng
Date: 10/9/2015

Provides several functions to encrypt and decrypt text using several encryption algorithms.
"""

def encrypt_caesar(plaintext):
    """
    Encrypts plaintext using a Caesar cipher.
    Add more implementation details here.
    """

    ciphertext = "";
    for letter in plaintext:
        letter = chr(ord(letter) + 3);
        if (not letter.isalpha()):
            letter = chr(ord(letter) - 26);
        ciphertext += letter;
    return ciphertext

def decrypt_caesar(ciphertext):
    """
    Decrypts a ciphertext using a Caesar cipher.
    Add more implementation details here.
    """

    plaintext = "";
    for letter in ciphertext:
        letter = chr(ord(letter) - 3);
        if (not letter.isalpha()):
            letter = chr(ord(letter) + 26);
        plaintext += letter;
    return plaintext

def encrypt_vigenere(plaintext, keyword):
    """
    Encrypts plaintext using a Vigenere cipher with a keyword.
    Add more implementation details here.
    """

    ciphertext = ""
    for i in range(0, len(plaintext)):
        #The following simplifies some of the addition for determining the enciphering
        #In the middle of the letter 'b' with keyword letter 'L', it's ('b' - 'a' + 'L' - 'A') + 'a' = 'b' + 'L' - 'A'
        letter = chr(ord(plaintext[i]) + ord(keyword[i % len(keyword)]) - ord('a' if keyword[i % len(keyword)].islower() else 'A'))
        #In short, this tests whether adding the keyword to the letter makes it need to loop around
        if ((not letter.isalpha()) or (letter.islower() and plaintext[i].isupper()) or (letter.isupper() and plaintext[i].islower())):
            letter = chr(ord(letter) - 26);
        ciphertext += letter;
    return ciphertext

def decrypt_vigenere(ciphertext, keyword):
    """
    Decrypts ciphertext using a Vigenere cipher with a keyword.
    Add more implementation details here.
    """

    plaintext = ""
    for i in range(0, len(ciphertext)):
        letter = chr(ord(ciphertext[i]) - ord(keyword[i % len(keyword)]) + ord('a' if keyword[i % len(keyword)].islower() else 'A'))
        if ((not letter.isalpha()) or (letter.islower() and ciphertext[i].isupper()) or (letter.isupper() and ciphertext[i].islower())):
            letter = chr(ord(letter) + 26);
        plaintext += letter;
    return plaintext

def encrypt_railfence(plaintext, num_rails):
    """
    Encrypts plaintext using a railfence cipher.
    Add more implementation details here.
    """

    if num_rails == 1:
        return plaintext
    ciphertext = ''
    rails = []
    for i in range(num_rails):
        rails.append([])
    counter = 0
    increase = True
    for letter in plaintext:
        rails[counter] += letter
        if increase:
            counter += 1
            if counter == num_rails:
                counter -= 2
                increase = not increase
        else:
            counter -= 1
            if counter == -1:
                counter += 2
                increase = not increase
    for rail in rails:
        ciphertext += ''.join(rail)
    return ciphertext


def decrypt_railfence(ciphertext, num_rails):
    """
    Encrypts plaintext using a railfence cipher.
    Add more implementation details here.
    """

    if num_rails == 1:
        return ciphertext
    plaintext = ''
    num_on_rails = []
    for i in range(num_rails):
        num_on_rails.append(0)

    counter = 0
    increase = True
    for letter in ciphertext:
        num_on_rails[counter] += 1
        if increase:
            counter += 1
            if counter == num_rails:
                counter -= 2
                increase = not increase
        else:
            counter -= 1
            if counter == -1:
                counter += 2
                increase = not increase

    rails = []
    startCount = 0
    endCount = 0
    for i in range(num_rails):
        endCount += num_on_rails[i]
        rails.append(list(ciphertext[startCount:endCount:]))
        startCount += num_on_rails[i]

    counter = 0
    increase = True
    for letter in ciphertext:
        plaintext += rails[counter].pop(0)
        if increase:
            counter += 1
            if counter == num_rails:
                counter -= 2
                increase = not increase
        else:
            counter -= 1
            if counter == -1:
                counter += 2
                increase = not increase

    return plaintext

def read_from_file(filename):
    """
    Reads and returns content from a file.
    Add more implementation details here.
    """
    
    with open(filename, 'r') as iffy: 
        content = iffy.readlines()
    return ' '.join(content) #concatenates all of the lines in the file together as a single string

def write_to_file(filename, content):
    """
    Writes content to a file.
    Add more implementation details here.
    """
    with open(filename, 'w') as offy: 
        offy.write(content)

def clean_input(str):
    newstr = ''
    for char in str:
        if (char.isalpha()):
            newstr += char
    return newstr

def run_suite():
    """
    Runs a single iteration of the cryptography suite.

    Asks the user for input text from a string or file, whether to encrypt
    or decrypt, what tool to use, and where to show the output.
    """
    print('Welcome to the Cryptography Suite!')
    print("*Input*")
    file_or_string = input('(F)ile or (S)tring? ').lower()
    while not (file_or_string == 'f' or file_or_string == 's'):
        file_or_string = input('(F)ile or (S)tring? ').lower()

    input_text = ''
    filename = ''
    if file_or_string == 'f':
        filename = input('Filename? ')
        input_text = read_from_file(filename)
    else:
        input_text = input('Enter the string to (en/de)crypt: ')

    input_text = clean_input(input_text)

    print("*Transform*")
    encrypt_or_decrypt = input('(E)ncrypt or (D)ecrypt? ').lower()
    while not (encrypt_or_decrypt == 'e' or encrypt_or_decrypt == 'd'):
        encrypt_or_decrypt = input('(E)ncrypt or (D)ecrypt? ').lower()

    crypt_type = input('(C)aesar, (V)igenere, or (R)ailfence? ').lower()
    while not (crypt_type == 'c' or crypt_type == 'v' or crypt_type == 'r'):
        crypt_type = input('(C)aesar, (V)igenere, or (R)ailfence? ').lower()

    inputStr = ''
    if file_or_string == 'f':
        inputStr = 'contents of ' + filename
    else:
        inputStr = input_text

    encr_or_decr = ''
    if encrypt_or_decrypt == 'e':
        encr_or_decr = 'Encrypting'
    else:
        encr_or_decr = 'Decrypting'

    cipher = ''
    passkey = ''
    rail_num = ''
    if crypt_type == 'c':
        cipher = 'Caesar cipher'
    elif crypt_type == 'v':
        passkey = input("Passkey? ")
        cipher = 'Vigenere cipher with key ' + passkey
    else:
        rail_num = int(input("Number of rails? "))
        cipher = 'railfence cipher'

    print(encr_or_decr, inputStr, 'using', cipher)
    print('...')

    print("*Output*")

    result_text = ''
    if crypt_type == 'c':
        if encrypt_or_decrypt == 'e':
            result_text = encrypt_caesar(input_text)
        else:
            result_text = decrypt_caesar(input_text)
    elif crypt_type == 'v':
        if encrypt_or_decrypt == 'e':
            result_text = encrypt_vigenere(input_text, passkey)
        else:
            result_text = decrypt_vigenere(input_text, passkey)
    else:
        if encrypt_or_decrypt == 'e':
            result_text = encrypt_railfence(input_text, rail_num)
        else:
            result_text = decrypt_railfence(input_text, rail_num)


    file_or_string = input('(F)ile or (S)tring? ').lower()
    while not (file_or_string == 'f' or file_or_string == 's'):
        file_or_string = input('(F)ile or (S)tring? ').lower()

    if file_or_string == 'f':
        filename = input('Filename? ')
        write_to_file(filename, result_text)
        print('Writing ciphertext to ', filename, '...')
    else:
        if encrypt_or_decrypt == 'e':
            encr_or_decr = 'ciphertext'
        else:
            encr_or_decr = 'plaintext'   
        print('The', encr_or_decr, 'is: ', result_text, '')





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
