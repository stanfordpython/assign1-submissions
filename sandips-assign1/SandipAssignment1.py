"""
Assignment 1: Cryptography
Course: CS 92SI
Name: SANDIP SRINIVAS
Date: 7 OCTOBER 2015

This program implements multiple cryptography types: caesar, vigniere, and Railfence.
The program gives the user the option of encrypting/decrypting into a file or string,
and gives output accordingly.
"""

def encrypt_caesar(plaintext):
    mapping = {}
    for number in range(97, 122):
        if (number < 120):
            mapping[chr(number)] = chr(number + 3)
        else:
            mapping[chr(number)] = chr(97 + (number - 120))
    ciphertext = ""
    for letter in plaintext:
        ciphertext += mapping[letter]
    return ciphertext

def decrypt_caesar(ciphertext):
    mapping = {}
    for number in range(97, 122):
        if (number > 100):
            mapping[chr(number)] = chr(number - 3)
        else:
            mapping[chr(number)] = chr(122 - (99 - number))
    plaintext = ""
    for letter in ciphertext:
            plaintext += mapping[letter]
    return plaintext


def encrypt_vigenere(plaintext, keyword):
    mapping = {}
    for number in range(1, 26):
        mapping[chr(number + 96)] = number
    ciphertext = ""
    for index in range(0, len(plaintext)):
        ciphertext += chr(((mapping[plaintext[index]] + mapping[keyword[index]]) % 26) + 95)
    return ciphertext
 

def decrypt_vigenere(ciphertext, keyword):
    print(ciphertext)
    print(keyword)
    mapping = {}
    for number in range(1, 26):
        mapping[chr(number + 96)] = number
    plaintext = ""
    for index in range(0, len(ciphertext)):
        if (mapping[ciphertext[index]] >= mapping[keyword[index]]):
            plaintext += chr(mapping[ciphertext[index]] - mapping[keyword[index]] + 97)
        else:
            plaintext += chr(27 - abs(mapping[ciphertext[index]] - mapping[keyword[index]]) + 96)
    return plaintext


def encrypt_railfence(plaintext, num_rails):
    ciphertext = ""
    indexAdjust = 2
    for rail in range(1, num_rails + 1):
        index = rail - 1  
        if (rail == 1 or rail == num_rails):
            ciphertext += plaintext[rail-1:len(plaintext):2*(num_rails -1)]
        else:
            ciphertext += plaintext[rail - 1]
            while (index < len(plaintext) - 1):
                index += ((2*(num_rails -1)))
                if (num_rails != 3): index -= indexAdjust
                if (    index < len(plaintext) - 1):
                    ciphertext += plaintext[index]               
                    index += ((2*(num_rails -1)) - indexAdjust + 2)
                    if (index < len(plaintext) - 1):
                        ciphertext += plaintext[index]
            indexAdjust += 2
    return ciphertext

def decrypt_railfence(ciphertext, num_rails):
    plaintext = ciphertext[0]
    index = 0
    adjust1 = 0
    while (len(plaintext) < len(ciphertext)):
        index += (int)(len(ciphertext) / num_rails) - 1 + adjust1
        if (index < len(ciphertext)):
            plaintext += ciphertext[index]
            index += (int)(len(ciphertext) / (num_rails - 1)) - adjust1
            if (index < len(ciphertext)):
                plaintext += ciphertext[index]
                index -= (int)(len(ciphertext) / (num_rails - 1)) - adjust1 - 1
                if (index < len(ciphertext)):
                    plaintext += ciphertext[index]
                    index -= (int)(len(ciphertext) / num_rails) - 1 + adjust1
                    if (index < len(ciphertext)):
                        plaintext += ciphertext[index]
                        ++adjust1

    print(plaintext)


def read_from_file(filename):
    with open(filename, 'r') as f:
        content = f.read()
    return str(content)


def write_to_file(filename, content):
     with open(filename, 'w') as f:
        f.write(content)

def run_suite():
    """
    Runs a single iteration of the cryptography suite.

    Asks the user for input text from a string or file, whether to encrypt
    or decrypt, what tool to use, and where to show the output.
    """
    print("*Input*")
    fileOrString = input("(F)ile or (S)tring? ")
    fileOrString = fileOrString.lower()
    while (not fileOrString.isalpha() or len(fileOrString) != 1 or 
        fileOrString not in ['f', 's']):
            fileOrString = input("Please enter either an F for File or an S for String: ")
            fileOrString = fileOrString.lower()
    if (fileOrString == 'f'):
        filename = input("Filename? ")
        name = read_from_file(filename)
    else: 
        name = input("Enter the string to encrypt: ")
    
    print("*Transform*")
    encryptOrDecrypt = input("(E)ncrypt or (D)ecrypt? ")
    encryptOrDecrypt = encryptOrDecrypt.lower()
    while (not encryptOrDecrypt.isalpha() or len(encryptOrDecrypt) != 1 or 
        encryptOrDecrypt not in ['e', 'd']):
            encryptOrDecrypt = input("Please enter either an E for Encrypt or an D for Decrypt: ")
            encryptOrDecrypt = encryptOrDecrypt.lower()

    cipherType = input("(C)aesar, (V)igenere, or (R)ailfence? ")
    cipherType = cipherType.lower()
    while (not cipherType.isalpha() or len(cipherType) != 1 or
        cipherType not in ['c', 'v', 'r']): 
            cipherType = input("Please enter either a C for Caesar, V for Vigniere, or R for Railfence: ")
            cipherType = cipherType.lower()

    if (cipherType == 'c'):
        if (encryptOrDecrypt == 'e'):
            print("Encrypting", name, "using Caesar cipher")
            output = encrypt_caesar(name.lower())
        if (encryptOrDecrypt == 'd'):
            print("Decrypting", name, "using Caesar cipher")
            output = decrypt_caesar(name.lower())

    if (cipherType == 'v'):
        passkey = input("Passkey? ")
        while (not passkey.isalpha()):
            passkey = input("Please enter a passkey of only English letters: ")
        if len(passkey) < len(name): 
            difference = len(name) - len(passkey)
            for index in range(0, difference):
                passkey += passkey[index%len(name)]
        if len(passkey) > len(name):
            passkey = passkey[:len(name)-1]
        if (encryptOrDecrypt == 'e'):
            print("Encrypting", name, "using Vigniere cypher with key", passkey)
            output = encrypt_vigenere(name.lower(), passkey.lower())
        if (encryptOrDecrypt == 'd'):
            print("Decrypting", name, "using Vigniere cypher with key", passkey)
            output = decrypt_vigenere(name.lower(), passkey.lower())
           
    if (cipherType == 'r'):
        rails = input("Enter number of rails: ")
        while (not rails.isnumeric):
            rails  = input("Please enter a positive integer number of rails: ")
        if (encryptOrDecrypt == 'e'): 
            print("Encrypting", name, "using Railfence cipher with", rails, "rails")
            output = encrypt_railfence(name, int(rails))
        if (encryptOrDecrypt == 'd'):
            print("Decrypting", name, "using Railfence cipher with", rails, "rails")
            output = decrypt_railfence(name, int(rails))
           
    print("*Output*")
    fileOrString = input("(F)ile or (S)tring? ")
    fileOrString = fileOrString.lower()
    while (not fileOrString.isalpha() or len(fileOrString) != 1 or 
        fileOrString not in ['f', 's']):
            fileOrString = input("Please enter either an F for File or an S for String: ")
            fileOrString = fileOrString.lower()
    if (fileOrString == 'f'): name = input("Filename? ")
    else: print(output)  # Print or write the transformed output


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