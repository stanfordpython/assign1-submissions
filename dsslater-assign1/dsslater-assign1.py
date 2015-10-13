"""
Assignment 1: Cryptography
Course: CS 92SI
Name: David Slater
Date: 10/6/15

Replace this with a description of the program.
"""
import re

def encrypt_caesar(plaintext):
    """
    Encrypts plaintext using a Caesar cipher.
    Add more implementation details here.
    """
    regex = re.compile('[^a-zA-z]')
    plaintext = regex.sub('', plaintext)

    caesar_map = {}
    for letter in range(ord('a'), ord('z') + 1):
        crypt = (letter + 3)
        if crypt > ord('z'):
            crypt -= (ord('z') + 1)
            crypt += ord('a')
        caesar_map[chr(letter)] = chr(crypt)
    for letter in range(ord('A'), ord('Z') + 1):
        crypt = (letter + 3)
        if crypt > ord('Z'):
            crypt -= (ord('Z') + 1)
            crypt += ord('A')
        caesar_map[chr(letter)] = chr(crypt)

    encrypted = ""
    for letter in plaintext:
        encrypted += str(caesar_map[letter])
    return encrypted


def decrypt_caesar(ciphertext):
    """
    Decrypts a ciphertext using a Caesar cipher.
    Add more implementation details here.
    """
    regex = re.compile('[^a-zA-z]')
    ciphertext = regex.sub('', ciphertext)

    caesar_map = {}
    for letter in range(ord('a'), ord('z') + 1):
        crypt = (letter - 3)
        if crypt < ord('a'):
            crypt += (ord('z') + 1)
            crypt -= ord('a')
        caesar_map[chr(letter)] = chr(crypt)
    for letter in range(ord('A'), ord('Z') + 1):
        crypt = (letter - 3)
        if crypt < ord('A'):
            crypt += (ord('Z') + 1)
            crypt -= ord('A')
        caesar_map[chr(letter)] = chr(crypt)
    
    plain = ""
    for letter in ciphertext:
        plain += str(caesar_map[letter])
    return plain


def encrypt_vigenere(plaintext, keyword):
    """
    Encrypts plaintext using a Vigenere cipher with a keyword.
    Add more implementation details here.
    """
    
    regex = re.compile('[^a-zA-z]')
    plaintext = regex.sub('', plaintext).upper()
    keyword = regex.sub('', keyword).upper()

    plain_len = len(plaintext)
    key_len = len(keyword)
    mult = (plain_len//key_len) + 1
    encrypt_str = keyword * mult
    diff = plain_len - len(encrypt_str)
    encrypt_str = encrypt_str[:diff]

    final_str = ""
    for i in range(len(plaintext)):
        new_letter = ord(plaintext[i]) + ord(encrypt_str[i]) - ord('A')
        if new_letter > ord('Z'):
            new_letter -= (ord('Z') + 1)
            new_letter += ord('A')
        final_str += str(chr(new_letter))

    return final_str


def decrypt_vigenere(ciphertext, keyword):
    """
    Decrypts ciphertext using a Vigenere cipher with a keyword.
    Add more implementation details here.
    """
    regex = re.compile('[^a-zA-z]')
    ciphertext = regex.sub('', ciphertext).upper()
    keyword = regex.sub('', keyword).upper()

    cipher_len = len(ciphertext)
    key_len = len(keyword)
    mult = (cipher_len//key_len) + 1
    encrypt_str = keyword * mult
    diff = cipher_len - len(encrypt_str)
    encrypt_str = encrypt_str[:diff]

    final_str = ""
    for i in range(len(ciphertext)):
        new_letter = ord(ciphertext[i]) - ord(encrypt_str[i]) + ord('A')
        if new_letter < ord('A'):
            new_letter += (ord('Z') + 1)
            new_letter -= ord('A')
        final_str += str(chr(new_letter))

    return final_str


def encrypt_railfence(plaintext, num_rails):
    """
    Encrypts plaintext using a railfence cipher.
    Add more implementation details here.
    """

    regex = re.compile('[^a-zA-z]')
    plaintext = regex.sub('', plaintext)

    text = plaintext
    data = {}
    for n in range(num_rails):
        data[n] = ""
    while(text != None):
        text = recursive_rails(0,num_rails - 1, data, text)
        if(text == None):
            continue
        text = data[0][-1] + text
        data[0] = data[0][0:-1]
    final_str = ""
    for key in data.keys():
        final_str += data[key]
    return final_str


def decrypt_railfence(ciphertext, num_rails):
    """
    Encrypts plaintext using a railfence cipher.
    Add more implementation details here.
    """
    regex = re.compile('[^a-zA-z]')
    ciphertext = regex.sub('', ciphertext)

    text = ciphertext
    data = {}
    for n in range(num_rails):
        data[n] = ""
    while(text != None):
        text = recursive_rails(0,num_rails - 1, data, text)
        if(text == None):
            continue
        text = data[0][-1] + text
        data[0] = data[0][0:-1]
    
    text = ciphertext
    new_data = {}
    for key in data.keys():
        new_data[key] = text[0:len(data[key])]
        text = text[len(data[key]):]

    plaintext =""
    target_length = len(ciphertext)

    while(len(plaintext) < target_length):
        for n in range(num_rails):
            if(len(plaintext) == target_length):
                break
            plaintext += new_data[n][0]
            new_data[n] = new_data[n][1:]
        for n in reversed(range(num_rails - 1)):
            if(len(plaintext) == target_length):
                break
            if(n != 0):
                plaintext += new_data[n][0]
                new_data[n] = new_data[n][1:]
    return plaintext

 
def recursive_rails(depth, target_depth, data, text):
    """
    Recursively breaks up a text into it's respective rails
    """
    if(len(text) < 1): #If you have reached the end of the text exit the recursion
        return None

    data[depth] += text[0] #grab letter for this rail
    text = text[1:]       #slice off letter from text

    if (depth == target_depth): #If this is the bottom of a trough return
        return text
    else:
        text = recursive_rails(depth + 1, target_depth, data, text) #Otherwise keep diving
        if(text == None): #If at some point in the dive the text ends the None will carry up stream to end the recursion
            return None
        data[depth] += text[0] #if the text did not end on the dive then slice off another
        text = text[1:]
        return text


def read_from_file(filename):
    """
    Reads and returns content from a file.
    Add more implementation details here.
    """
    with open(filename, 'r') as f:
        lines = f.readlines()
    final_str = ""
    for line in lines:
        final_str += line

    return final_str


def write_to_file(filename, content):
    """
    Writes content to a file.
    Add more implementation details here.
    """
    with open(filename,'w') as f:
        f.write(content)


def run_suite():
    """
    Runs a single iteration of the cryptography suite.

    Asks the user for input text from a string or file, whether to encrypt
    or decrypt, what tool to use, and where to show the output.
    """
    
    text = ""

    text_input = input("Will you be using text?(Y/N) ").upper()
    while(text_input != "Y" and text_input != "N"):
        text_input = input("Sorry, that was not a valid response. Will you be using text?(Y/N)").upper()

    
    
    if(text_input == "Y"):
        text = input("What is the text? ")
    else:
        file_name = input("What file name? ")
        text = read_from_file(file_name)
    
    action = input("\nWhich transformation would you like to apply to the input?\n(1) Encrypt Caesar\n(2) Decrypt Caesar\n(3) Encrypt Vigenere\n(4) Decrypt Vigenere\n(5) Encrypt Railfence\n(6) Decrypt Railfence\n")
    while(action != "1" and action != "2" and action != "3" and action != "4" and action != "5" and action != "6"):
        action = input("\nSorry, that was not a valid response. Which transformation would you like to apply to the input?\n(1) Decrypt Caesar\n(2) Encrypt Caesar\n(3) Encrypt Vigenere\n(4) Decrypt Vigenere\n(5) Encrypt Railfence\n(6) Decrypt Railfence\n")
    
    result = ""
    if (action == "1"):
        result = encrypt_caesar(text)
    elif (action == "2"):
        result = decrypt_caesar(text)
    elif (action == "3"):
        key = input("What is the vigenere key? ")
        result = encrypt_vigenere(text, key)
    elif (action == "4"):
        key = input("What is the vigenere key? ")
        result = decrypt_vigenere(text, key)
    elif (action == "5"):
        num_rails = input("How many rails? ")
        result = encrypt_railfence(text, int(num_rails))
    elif (action == "6"):
        num_rails = input("How many rails? ")
        result = decrypt_railfence(text, int(num_rails))
    
    print(result)

    write_out = input("Would you like to write out result?(Y/N) ").upper()
    while(write_out != "Y" and write_out != "N"):
        write_out = input("Sorry, that was not a valid response. Would you like to write out result? (Y/N) ").upper()

    out_file_name = ""
    if(write_out == "Y"):
        out_file_name = input("What output file name? ")

    if(write_out == "Y"):
        write_to_file(out_file_name, result)


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
