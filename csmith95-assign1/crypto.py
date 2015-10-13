"""
Assignment 1: Cryptography
Course: CS 92SI
Name: Conner Smith
Date: 10/9/15

This program encrypts/decrypts plaintext using either 
Caesar's cipher, Vigenere's cipher, or railfence cipher
"""
import string

LETTERS_IN_ALPHABET = 26

# a dictionary of char-to-char mappings for 
# Caesar's cipher
letterMappings = {}
reverseLetterMappings = {}

# returns character that originalLetter maps to given an offset. Assumes originalLetter
# is lowercase
def computeNewLetter(originalLetter, offset):
    encryptedLetterOffset = (ord(originalLetter) - ord('a') + offset) % LETTERS_IN_ALPHABET
    # deal with the case of decrypting using vigenere's cipher when letters must wrap around to from 
    # beginning to end of alphabet
    if encryptedLetterOffset < 0:
        return chr(ord('z') + encryptedLetterOffset)
    return chr(ord('a') + encryptedLetterOffset)


# fills dictionaries with letter mappings for caesar's cipher
def constructLetterMappingsForCaesar():
    for offset in range(LETTERS_IN_ALPHABET):
        key = chr(ord('a') + offset)
        val = computeNewLetter(key, 3)
        letterMappings[key] = val
        reverseLetterMappings[val] = key

# encrypts plaintext and returns result in all uppercase
def encrypt_caesar(plaintext):
    encrypted = ''
    for ch in plaintext.lower():
        encrypted += letterMappings[ch]
    return encrypted.upper()

# decrypts ciphertext and returns result in all uppercase
def decrypt_caesar(ciphertext):
    decrypted = ''
    for ch in ciphertext.lower():
        decrypted += reverseLetterMappings[ch]
    return decrypted.upper()


# encrypts plaintext using a Vigenere cipher with a keyword.
def encrypt_vigenere(plaintext, keyword):
    encrypted = ''
    # convert keyword to lowercase string without spaces
    keyword = keyword.lower().replace(" ", "")
    for (index, ch) in enumerate(plaintext.lower()):
        indexInKeyword = index % len(keyword)
        offset = ord(keyword[indexInKeyword]) - ord('a')
        encrypted += computeNewLetter(ch, offset)
    return encrypted.upper()

# decrypts plaintext using a Vigenere cipher with a keyword.
def decrypt_vigenere(ciphertext, keyword):
    decrypted = ''
    # convert keyword to lowercase string without spaces
    keyword = keyword.lower().replace(" ", "")
    for (index, ch) in enumerate(ciphertext.lower()):
        indexInKeyword = index % len(keyword)
        offset = ord('a') - ord(keyword[indexInKeyword])
        decrypted += computeNewLetter(ch, offset)
    return decrypted.upper()

# encrypts plaintext using a railfence cipher.
def encrypt_railfence(plaintext, num_rails):
    # handle edge cases
    if num_rails == 0 or num_rails == 1:
        return plaintext

    encrypted = ''
    # construct a list of step_sizes in which the index in the 
    # list corresponds to the step_size for that row. For the last row, 
    # step_size should loop around to the 0th index
    step_sizes = [x for x in range( (2 * num_rails) - 2, 0, -2)]
    text_length = len(plaintext)
    for rail_num in range(num_rails):
        step_size = step_sizes[rail_num % (num_rails - 1)]
        encrypted += plaintext[rail_num : text_length : step_size]
    return encrypted.upper()



""" this doesn't work at all.. I spent way too much time failing. I think all of the
    other functions work """
# encrypts plaintext using a railfence cipher.
def decrypt_railfence(ciphertext, num_rails):
    # handle edge cases
    if num_rails == 0 or num_rails == 1:
        return ciphertext

    text_length = len(ciphertext)
    # create a list that contains each rail
    step_sizes = [x for x in range( (2 * num_rails) - 2, 0, -2)]
    rails = []
    start = 0
    for rail_num in range(num_rails):
        stop = int(text_length / num_rails) + 1 + start
        rail = ciphertext[start : stop]
        print(rail)
        rails.append(rail)
        start += len(rail)

    rails = ['wecrlte', 'erdsoeefeaoc', 'aivden']
    print(rails)


    decrypted = ''
    next_index_to_read = [0 for _ in range(num_rails)]
    curr_rail = 0
    for x in range(text_length):
        print(decrypted)
        print(curr_rail)
        print(next_index_to_read[curr_rail])
        index = next_index_to_read[curr_rail]
        decrypted += rails[curr_rail][index]
        next_index_to_read[curr_rail] += 1
        if curr_rail == num_rails - 1:
            offset = -1
        elif curr_rail == 0:
            offset = 1
        curr_rail = (curr_rail + offset) % num_rails

    return decrypted.upper()

# returns string indicating whether user wants to encrypt, decrypt, or quit
def promptForTask():
    task = 'z'
    while task not in ['e', 'd', 'q']:
        task = input("Would you like to (e)ncrypt, (d)ecrypt, or (q)uit? ")[0].lower()

    if task == 'e':
        return 'encrypt'
    if task == 'd':
        return 'decrypt'
    if task == 'q':
        return 'quit'

# returns string indicating whether user wants to use caesar's, vigenere's, or railfence
def promptForCipherToUse():
    choice = 'z'
    while choice not in ['c', 'v', 'r']:
        choice = input("Would you like to use (c)aesar's, (v)igenere's, or (r)ailfence? ")[0].lower()

    if choice == 'c':
        return 'caesar'
    if choice == 'v':
        return 'vigenere'
    if choice == 'r':
        return 'railfence'
    
# if user wants to use vigenere's this method returns a string to use as keyword. 
# if user wants to use railfence, this method returns an int to use as num_rails
def promptForAdditionalInfo(cipherToUse):
    if cipherToUse == 'vigenere':
        return input('Provide a key: ')
    return int(input('How many rails? '))

# returns text user wants to encrypt or decrypt
def promptForTextToUse():
    return input('Enter a string to encrypt/decrypt: ')

# returns copy of text without punctuation characters
def removePunctuationAndSpace(text):
    punctuation_set = set(string.punctuation)
    whitespace_set = set(string.whitespace)
    text = ''.join(ch for ch in text if ch not in punctuation_set and ch not in whitespace_set)
    return text.replace(" ", "")

def readingFromFile():
    response = input("Read from file [Y/N]? ")
    if response[0].lower() == 'y':
        return True
    return False

def writingToFile():
    response = input("Write to file [Y/N]? ")
    if response[0].lower() == 'y':
        return True
    return False


def openFile():
    filename = input("Enter a filename: ")
    return open(filename, 'r+')

def performEncryption(originalText, cipherToUse, additional, writeToFile, fw):
    if cipherToUse == 'caesar':
            output = encrypt_caesar(originalText)
    elif cipherToUse == 'vigenere':
        output = encrypt_vigenere(originalText, additional)
    else:
        output = encrypt_railfence(originalText, additional)

    # display result to user
    if writeToFile:
        fw.print('Transformed text: ' + output)
    else:
        print('Transformed text: ' + output)

def performDecryption(originalText, cipherToUse, additional, writeToFile, fw):
    if cipherToUse == 'caesar':
            output = decrypt_caesar(originalText)
    elif cipherToUse == 'vigenere':
        output = decrypt_vigenere(originalText, additional)
    else:
        output = decrypt_railfence(originalText, additional)

     # display result to user
    if writeToFile:
        fw.write('Transformed text: ' + output)
    else:
        print('Transformed text: ' + output)

def run_suite():
    """
    Runs a single iteration of the cryptography suite.

    Asks the user for input text from a string or file, whether to encrypt
    or decrypt, what tool to use, and where to show the output.
    """
    constructLetterMappingsForCaesar()
    # obtain task from user
    task = promptForTask();
    if task == 'quit':
        return

    readFromFile = False
    if readingFromFile():
        f = openFile()
        readFromFile = True
    else:
        originalText = promptForTextToUse()
        originalText = removePunctuationAndSpace(originalText)

    writeToFile = False
    fw = None
    if writingToFile():
        fw = openFile()
        writeToFile = True


    # obtain method from user
    cipherToUse = promptForCipherToUse()
    additional = 0
    if cipherToUse != 'caesar':
        additional = promptForAdditionalInfo(cipherToUse)

    # perform operation
    if task == 'encrypt':
        if readFromFile:
            for line in f:
                performEncryption(removePunctuationAndSpace(line), cipherToUse, additional, writeToFile, fw)
        else:
            performEncryption(originalText, cipherToUse, additional, writeToFile, fw)
    else: 
        if readFromFile:
            for line in f:
                performDecryption(removePunctuationAndSpace(line), cipherToUse, additional, writeToFile, fw)
        else:
            performDecryption(originalText, cipherToUse, additional, writeToFile, fw)


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
