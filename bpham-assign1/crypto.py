"""
Assignment 1: Cryptography
Course: CS 92SI
Name: Brexton Pham
Date: 10/9/15

Cryptography suite!
"""

import itertools

alphabetLower = "abcdefghijklmnopqrstuvwxyz"
alphabetUpper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def encrypt_caesar(plaintext):
    """
    Encrypts plaintext using a Caesar cipher.
    Add more implementation details here.
    """
    result = ""
    #print(alphabet)
    for letter in plaintext:
        if letter in alphabetUpper:
            result += alphabetUpper[(alphabetUpper.index(letter) + 3) % 26]
        else: 
            result += alphabetLower[(alphabetLower.index(letter) + 3) % 26]
    print(result)
    return result  


def decrypt_caesar(ciphertext):
    """
    #Decrypts a ciphertext using a Caesar cipher.
    #Add more implementation details here.
    """
    result = ""
    #print(alphabet)
    for letter in ciphertext:
        if letter in alphabetUpper:
            result += alphabetUpper[(alphabetUpper.index(letter) - 3) % 26]
        else: 
            result += alphabetLower[(alphabetLower.index(letter) - 3) % 26]
    print(result)
    return result  

def encrypt_vigenere(plaintext, keyword):
    """
    #Encrypts plaintext using a Vigenere cipher with a keyword.
    #Add more implementation details here.
    """
    print(plaintext)
    result = ""
    cycle = itertools.cycle(keyword)
    key = ""
    i = 0
    for letter in cycle:
        
        i += 1
        key += letter.lower()
        if i >= len(plaintext):
            break
    #print(alphabetLower.index(key[0]))
    j = 0
    for letter in plaintext:
        if letter in alphabetUpper:
            result += alphabetUpper[(alphabetUpper.index(letter) + alphabetLower.index(key[j])) % 26]
        else: 
            result += alphabetLower[(alphabetLower.index(letter) + alphabetLower.index(key[j])) % 26]
        j = j + 1
    print(result)
    return result


def decrypt_vigenere(ciphertext, keyword):
    """
    #Decrypts ciphertext using a Vigenere cipher with a keyword.
    #Add more implementation details here.
    """
    result = ""
    cycle = itertools.cycle(keyword)
    key = ""
    i = 0
    for letter in cycle:
        i += 1
        key += letter.lower()
        if i >= len(ciphertext):
            break
    #print(alphabetLower.index(key[0]))
    j = 0
    for letter in ciphertext:
        if letter in alphabetUpper:
            result += alphabetUpper[(alphabetUpper.index(letter) -  alphabetLower.index(key[j])) % 26]
        else: 
            result += alphabetLower[((alphabetLower.index(letter)) - (alphabetLower.index(key[j]))) % 26]
        j = j + 1
    print(result)
    return result

def encrypt_railfence(plaintext, num_rails):
    """
    #Encrypts plaintext using a railfence cipher.
    #Add more implementation details here.
    """
    result = [None] * len(plaintext)
    brextonIsSoCool = 2 * (num_rails - 1)
    tracker = 0
    counter = 0

    while counter < num_rails:

        size = brextonIsSoCool - 2 * counter
        i = counter
        equals = 1
        while i < len(plaintext):
            result[tracker] = plaintext[i] #switch
            
            if equals == 0 or (size == 0):
                i += (brextonIsSoCool - size)
            else:
                i += size

            if counter!= 0: 
                equals = 0

            tracker += 1
        counter += 1

    return "".join(result)

def decrypt_railfence(ciphertext, num_rails):
    """
    #Encrypts plaintext using a railfence cipher.
    #Add more implementation details here.
    """
    result = [None] * len(ciphertext)
    brextonIsSoCool = 2 * (num_rails - 1)
    tracker = 0
    counter = 0

    while counter < num_rails:

        size = brextonIsSoCool - 2 * counter
        i = counter
        equals = 1
        while i < len(ciphertext):
            result[i] = ciphertext[tracker] #switch
            
            if equals == 0 or (size == 0):
                i += (brextonIsSoCool - size)
            else:
                i += size

            if counter!= 0: 
                equals = 0

            tracker += 1
        counter += 1

    return "".join(result)

def read_from_file(filename):
    """
    #Reads and returns content from a file.
    #Add more implementation details here.
    """

    with open(filename, 'r') as f:
        content = f.read()

    return content



def write_to_file(filename, content):
    """
    #Writes content to a file.
    #Add more implementation details here.
    """
    # Your implementation here
    with open(filename, 'w') as f:
        f.write(content)

    


def run_suite():
    """
    #Runs a single iteration of the cryptography suite.

    #Asks the user for input text from a string or file, whether to encrypt
    #or decrypt, what tool to use, and where to show the output.
    """
    resultText = ""
    print("*Input*")
    desiredInput = input("(F)ile or (S)tring? ")
    while (desiredInput != "f" and desiredInput != "F" and desiredInput != "s" and desiredInput != "S"):
        desiredInput = input("Please input either S for string or F for file! ")
    string = ""
    if (desiredInput.upper() == "S"):
        string = input("Enter the string to de/encrypt: ")  # Obtain the user's desired input here
    elif (desiredInput.upper() == "F"):
        filename = input("Filename: ")
        string = read_from_file(filename)

    string = string.replace(" ", "")
    string = string.replace("!", "")
    string = string.replace("@", "")
    string = string.replace("#", "")
    string = string.replace("$", "")
    string = string.replace("%", "")
    string = string.replace("^", "")
    string = string.replace("&", "")
    string = string.replace("*", "")
    string = string.replace("(", "")
    string = string.replace(")", "")
    string = string.replace("-", "")
    string = string.replace("+", "")
    string = string.replace("=", "")
    string = string.replace("-", "")
    string = string.replace("[", "")
    string = string.replace("]", "")
    string = string.replace("{", "")
    string = string.replace("}", "")
    string = string.replace("|", "")
    string = string.replace(";", "")
    string = string.replace(":", "")
    string = string.replace("<", "")
    string = string.replace(">", "")
    string = string.replace(".", "")
    string = string.replace(",", "")
    string = string.replace("/", "")

    print("*Transform*")
    transform = input("(E)ncrypt or (D)ecrypt? ")
    while (transform != "e" and transform != "E" and transform != "d" and transform != "D"):
        transform = input("Please input either E for encrypt or D for decrypt! ")  # Encrypt or decrypt the input
    whichOne = input("(C)aesar, (V)igenere, or (R)ailfence? ")
    while (whichOne!= "C" and whichOne != "c" and whichOne != "V" and whichOne != "v" and whichOne != "r" and whichOne != "R"):
        whichOne = input("Please input either C for Caesar or V for Vigenere or R for Railfence! ")
    if (transform.upper() == "E" and whichOne.upper() == "V"):
        passkey = input("Passkey? ")
        print("Encrypting using Vigenere cipher!")
        resultText = encrypt_vigenere(string, passkey)
    elif (transform.upper() == "D" and whichOne.upper() == "V"):
        passkey = input("Passkey? ")
        print("Decrypting using Vigenere cipher!")
        resultText = decrypt_vigenere(string, passkey)
    elif (transform.upper() == "E" and whichOne.upper() == "C"):
        print("Encrypting using Caesar cipher!")
        resultText = encrypt_caesar(string)
    elif (transform.upper() == "D" and whichOne.upper() == "C"):
        print("Decrypting using Caesar cipher!")
        resultText = decrypt_caesar(string)
    elif (transform.upper() == "E" and whichOne.upper() == "R"):
        rails = input("Please enter a positive integer of rails! ")
        print("Encrypting using Railfence cipher!")
        resultText = encrypt_railfence(string, int(rails))
    elif (transform.upper() == "D" and whichOne.upper() == "R"):
        rails = input("Please enter a positive integer of rails! ")
        print("Decrypting using Railfence cipher!")
        resultText = decrypt_railfence(string, int(rails))


    print("*Output*")
    outputChoice = input("(F)ile or (S)tring? ") 
    while (outputChoice != "f" and outputChoice != "F" and outputChoice != "s" and outputChoice != "S"):
        outputChoice = input("Please input either S for string or F for file! ")
    end = ""
    if (outputChoice.upper() == "F"):
        end = input("Filename? ")
        print("Writing to file")
        write_to_file(end, resultText) # Print or write the transformed output
    elif(outputChoice.upper() == "S"):
        print(resultText)


# Do not modify code beneath this point.
def should_continue():
    """
    #Asks the user whether they would like to continue.
    #Responses that begin with a `Y` return True. (case-insensitively)
    #Responses that begin with a `N` return False. (case-insensitively)
    #All other responses (including '') cause a reprompt.
    """
    choice = input("Again (Y/N)? ").upper()
    while not choice or choice[0] not in ['Y', 'N']:
        choice = input("Please enter either 'Y' or 'N'. Again (Y/N)? ").upper()
    return choice[0] == 'Y'

#name = input("what is your name?")
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
