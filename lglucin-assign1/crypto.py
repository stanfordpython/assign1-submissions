"""
Assignment 1: Cryptography
Course: CS 92SI
Name: Lloyd Lucin
Date: 10/9/2015

This console program allows users to perform string encryption
and decryptions.  
Encryption styles are: Caesar, Vigenere, and 
Railfence.
Users may either type a string to encrypt/decrypt or provide
a text file.
"""

import string


def caesarEncryptMap():
    """
    Returns a dictionary where keys are capital letters
    of the alphabet and values are letters that are 
    'three away' from the key.  Wraps around for letters
    X, Y, and Z.
    """
    plainToEncryptedChars = {}
    for c in string.ascii_uppercase:
        if ord(c) >= ord('X'):
            refC = chr(ord(c) - len(string.ascii_uppercase))
        else:
            refC = c
        plainToEncryptedChars[c] = chr(ord(refC) + 3)
    return plainToEncryptedChars


def encrypt_caesar(plaintext):
    """
    Encrypts plaintext using a Caesar cipher.
    We create a dictionary that returns a dictionary
    of alphabets to their letter '3 spots ahead',
    which we use to build our encrypted string.
    """
    
    plainToEncryptedChars = caesarEncryptMap()

    encrypted = ""
    for c in plaintext:
        encrypted += plainToEncryptedChars[c.upper()]
    return encrypted


def decrypt_caesar(ciphertext):
    """
    Decrypts a ciphertext using a Caesar cipher.
    We take the dictionary from caesarEncryptMap() and
    reverse the key value pairs.  We then use this
    dictionary to decrypt our ciphertext.
    """
    plainToEncryptedChars = caesarEncryptMap()
    encryptedToPlainChars = dict(zip(plainToEncryptedChars.values(), plainToEncryptedChars.keys()))

    decrypted = ""
    for c in ciphertext:
        decrypted += encryptedToPlainChars[c.upper()]
    return decrypted



def encrypt_vigenere(plaintext, keyword):
    """
    Encrypts plaintext using a Vigenere cipher with a keyword.
    We encrypt each character through modular operations with the
    ASCII representation of each character.
    """
    encrypted = ""
    plaintext = plaintext.upper()
    keyword = keyword.upper()

    for i in range(len(plaintext)):
        alphaIndex = (ord(keyword[i%(len(keyword))]) + ord(plaintext[i]) - 2 * ord('A')) % 26
        encrypted += chr(alphaIndex + ord('A'))
    return encrypted


def decrypt_vigenere(ciphertext, keyword):
    """
    Decrypts ciphertext using a Vigenere cipher with a keyword.
    We decrypt each character through modular operations with the
    ASCII representation of each character.
    """
    decrypted = ""
    ciphertext = ciphertext.upper()
    keyword = keyword.upper()

    for i in range(len(ciphertext)):
        alphaIndex = (ord(ciphertext[i]) - ord(keyword[i%(len(keyword))])) % 26
        decrypted += chr(alphaIndex + ord('A'))
    return decrypted


def dotMatrix(num_rails, width):
    """
    Returns a num_railsXwidth matrix of all '.'
    """
    matrix = []
    for i in range(num_rails):
        l = ['.' for i in range(width)]
        matrix.append(l)
    return matrix


def encrypt_railfence(plaintext, num_rails):
    """
    Encrypts plaintext using a railfence cipher.
    We create a matrix of all '.' of size plaintextXnum_rails.
    We then insert characters of the plaintext into this
    matrix in railfence format.  Afterwards we build our
    encryption by reading each non '.' character across each 
    row of our matrix.
    """

    plaintext = plaintext.upper()

    # Special Case
    if num_rails == 1:
        return plaintext

    # Create matrix of '.'s
    matrix = dotMatrix(num_rails, len(plaintext))        
    leftDown = True
    r = 0
    c = 0

    # Insert letters into rails
    for i in range(len(plaintext)):
        matrix[r][c] = plaintext[i]
        if leftDown:
            r += 1
        else:
            r -= 1
        if r == 0 or r == (num_rails - 1):
            leftDown = not leftDown
        c += 1

    # Encrypt from Rails
    encrypted = ""
    for l in matrix:
        for c in l:
            if c != '.':
                encrypted += c;

    for line in matrix:
        print(line)
    return encrypted


def decrypt_railfence(ciphertext, num_rails):
    """
    Encrypts plaintext using a railfence cipher.
    Constructs the same railfence matrix from encrypt_railfence().
    It then, reads diagonally down and up moving right to decrypt
    the message.
    """

    ciphertext = ciphertext.upper()

    # Special Case
    if num_rails == 1:
        return ciphertext

    # Create Railfence matrix
    matrix = dotMatrix(num_rails, len(ciphertext))
    cipherIndex = 0
    step = 2 * num_rails - 2

    # For every list
    for i in range(len(matrix)):
        row = matrix[i]
        for j in range(len(row)):
            move = i + j * step
            if i != 0 and i != (num_rails - 1):
                move = i + j * step//2
                # For all odd values
                if j%2 != 0 and move < len(row):
                    if i < num_rails//2:
                        # Move right until you find a letter to the right and up in the matrix 
                        while move < len(ciphertext) - 2 and matrix[i - 1][move + 1] == '.':
                            move += 1
                    if i >= num_rails//2:
                        if i != num_rails//2 or num_rails%2 == 0:
                            # Move left until you find a letter to the right and up in the matrix
                            while move > 1 and matrix[i - 1][move + 1] == '.':
                                move -= 1
            # Insert the character of ciphertext into matrix
            if move < len(row):
                print("Assigning: " + str(i) + ", " +str(move))
                matrix[i][move] = ciphertext[cipherIndex]
                cipherIndex += 1

    # Read Diagonally to decrypt
    decrypted = ""
    leftDown = True
    r = 0
    c = 0
    for i in range(len(ciphertext)):
        decrypted += matrix[r][c]
        if leftDown:
            r += 1
        else:
            r -= 1
        if r == 0 or r == (num_rails - 1):
            leftDown = not leftDown
        c += 1

    for line in matrix:
        print(line)
    return decrypted


def read_from_file(filename):
    """
    Reads and returns content from a file.
    """
    with open(filename, 'r') as f:
        first_line = f.readline()  
    return first_line  


def write_to_file(filename, content):
    """
    Writes content to a file.
    """
    target = open(filename, 'w')
    target.write(content)


def keep_prompting(prompt, *validAnswers):
    """
    Keeps prompting the user until they provide
    a satisfactory answer.
    """
    answer = input(prompt)
    while answer.upper() not in validAnswers:
        print("Please respond with: ", end="") 
        print(''.join('\"{},\" '.format(*k) for k in validAnswers))
        answer = input(prompt)
    return answer.upper()

def run_suite():
    """
    Runs a single iteration of the cryptography suite.

    Asks the user for input text from a string or file, whether to encrypt
    or decrypt, what tool to use, and where to show the output.
    """
    print("Welcome to Cryptography Suite!")
    print("*Input*")
    fileOrString = keep_prompting("(F)ile or (S)tring? ", 'F', 'S')
    if fileOrString == 'S':
        usrInput = input("Enter the string to encrypt: ")
        usrInput = ''.join(ch for ch in usrInput if ch.isalnum())
    else:
        usrInput = read_from_file(input("Filename: "))
    print("*Transform*")
    encrypt = keep_prompting("(E)ncrypt or (D)ecrypt? ", 'E', 'D') == 'E'
    encryptionStyle = keep_prompting("(C)aesar, (V)igenere, or (R)ailfence? ", "C", "V", "R")
    if encryptionStyle == "C":
        if encrypt:
            output = encrypt_caesar(usrInput)
        else:
            output = decrypt_caesar(usrInput)
    if encryptionStyle == "V":
        keyword = input("Passkey? ")
        if encrypt:
            output = encrypt_vigenere(usrInput, keyword)
        else:
            output = decrypt_vigenere(usrInput, keyword)
    if encryptionStyle == "R":
        num_rails = int(input("Number of rails? "))
        if encrypt:
            output = encrypt_railfence(usrInput, num_rails)
        else:
            output = decrypt_railfence(usrInput, num_rails)

    print("*Output*")
    writeFile = keep_prompting("(F)ile or (S)tring? ", 'F', 'S') == 'F'
    if writeFile:
        write_to_file(input("Filename: "), output)
    else:
        print(output)


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
