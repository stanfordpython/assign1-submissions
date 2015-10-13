"""
Assignment 1: Cryptography
Course: CS 92SI
Name: GEOFFREY ANGUS
Date: 10/7/2015

Replace this with a description of the program.
"""

def encrypt_caesar(plaintext):
    """
    Encrypts plaintext using a Caesar cipher.
    Add more implementation details here.
    """
    
    ciphertext = []
    for letter in plaintext:
        ciphertext.append(chr(((ord(letter) - 62) % 26) + 65))
    outputString = ''.join(ciphertext)

    # plaintext:
    # PYTHON
    # ciphertext:
    # SBWKRQ

    return outputString


def decrypt_caesar(ciphertext):
    """
    Decrypts a ciphertext using a Caesar cipher.
    Add more implementation details here.
    """
    
    plaintext = []
    for letter in ciphertext:
        plaintext.append(chr(((ord(letter) + 36) % 26) + 65))
    outputString = ''.join(plaintext)
    return outputString


def encrypt_vigenere(plaintext, keyword):
    """
    Encrypts plaintext using a Vigenere cipher with a keyword.
    Add more implementation details here.
    """
    key = []
    index = 0

    ciphertext = []
    for i in range(len(plaintext)):
        index = i % len(keyword)
        key = keyword[index]
        ciphertext.append(chr((ord(plaintext[i])+ord(key)) % 26 + 65))
    outputString = ''.join(ciphertext)

    # plaintext:
    # ATTACKATDAWN
    # key:
    # LEMONLEMONLE
    # ciphertext:
    # LXFOPVEFRNHR
    return outputString


def decrypt_vigenere(ciphertext, keyword):
    """
    Decrypts ciphertext using a Vigenere cipher with a keyword.
    Add more implementation details here.
    """
    key = []
    index = 0

    plaintext = []
    for i in range(len(ciphertext)):
        index = i % len(keyword)
        key = keyword[index]
        plaintext.append(chr((ord(ciphertext[i])-ord(key)) % 26 + 65))
    outputString = ''.join(plaintext)

    return outputString

def encrypt_railfence(plaintext, num_rails):
    """
    Encrypts plaintext using a railfence cipher.
    Add more implementation details here.
    """
    level = 0
    direction = -1

    cipherlist = [[] for _ in range(num_rails)]
    for letter in plaintext:
        cipherlist[level].append(letter)
        if level > num_rails - 2:
            direction = -direction
        elif level < 1:
            direction = -direction
        level = level + direction
    
    ciphertext = []
    for i in cipherlist:
        ciphertext.append(''.join(i))

    outputString = ''.join(ciphertext)

    # plaintext:
    # WEAREDISCOVEREDFLEEATONCE
    # num_rails:
    # 3
    # ciphertext:
    # WECRLTEERDSOEEFEAOCAIVDEN

    return outputString


def decrypt_railfence(ciphertext, num_rails):
    """
    Encrypts plaintext using a railfence cipher.
    Add more implementation details here.
    """

    spacing = num_rails + num_rails - 2
    segmentLength = num_rails - 1
    numSegments = len(ciphertext) // segmentLength
    numRepetition = len(ciphertext) // spacing
    numLeftover = len(ciphertext) % segmentLength

    isAscending = numSegments % 2

    plainlist = [[] for _ in range(spacing)]

    if isAscending:
        numsFromEnd = len(ciphertext) - numRepetition - 1
    else:
        numsFromEnd = len(ciphertext) - numRepetition

    plainlist[spacing - 1] = ciphertext[numsFromEnd:]

    i = 0
    count = 0
    plainbucket = 0
    leftOverlist = []
    for j in range(spacing - 1):
        if (i < numsFromEnd - numRepetition):
            plainlist[j] = ciphertext[i:i + numRepetition + 1]
        else:
            plainlist[j] = ciphertext[i:numsFromEnd]
        if i + numRepetition + 1 < numsFromEnd - 1:
            i += numRepetition + 1
        else:
            i += 1
        if (numLeftover > 0):
            leftOverlist += ciphertext[i]
            numLeftover -= 1
    mergeMid = plainlist[1] + plainlist[2]
    plainlist = [plainlist[0],mergeMid,plainlist[3]]
    i = 0
    plaintext = [None] * (len(ciphertext))
    for level in range(spacing):
        if (level == 0 or level == segmentLength):
            plaintext[level::spacing] = plainlist[level]
        else:
            plaintext[level::spacing] = mergeMid[i // 2::2]
        i += 1
    return ''.join(plaintext)


    # i = 0
    # segmentLength = num_rails - 1
    # numSegments = len(ciphertext) // segmentLength
    # numLeftover = len(ciphertext) % segmentLength
    # isAscending = numSegments % 2
    # count = 0
    # segment = 0
    # plainList = [None] * len(ciphertext)
    # for letters in ciphertext:
    #     offset = count % segmentLength * 2
    #     if offset == 0:
    #         plainList[offset::spacing] = ciphertext[segment:segment + numSegments//2]
    #         segment += numSegments/2

    #     else:
    #         plainList[offset::spacing] = ciphertext[segment:segment + numSegments:2]
    #         segment

    #     count += 1

def read_from_file(filename):
    """
    Reads and returns content from a file.
    Add more implementation details here.
    """
    l = []
    with open(filename) as f:
        for line in f:
            line = line.upper()
            l.append(line)
    str1 = ''.join(l)
    return str1


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
    inputType = input('(F)ile or (S)tring? ').upper() # Obtain the user's desired input here
    while not inputType or inputType[0] not in ['F','S']:
        inputType = input('(F)ile or (S)tring? ').upper()
    if inputType[0] == 'S':
        inputString = input('Enter the string to encrypt: ').upper()
    else:
        inputString = read_from_file(input('Enter the file to encrypt: ')).upper()

    inputString = ''.join([i for i in inputString if i.isalpha()])
    print (inputString)


    print("*Transform*")
    inputType = input('(E)ncrypt or (D)ecrypt? ').upper() # Encrypt or decrypt the input
    while not inputType or inputType[0] not in ['E','D']:
        inputType = input('(E)ncrypt or (D)ecrypt? ').upper()

    cipherType = input('(C)aesar, (V)igenere, or (R)ailfence? ').upper()
    while not cipherType or cipherType[0] not in ['C','V','R']:
        cipherType = input('(C)aesar, (V)igenere, or (R)ailfence? ').upper()
    if cipherType[0] == 'C':
        print("It's a Caesar cipher!")
        if inputType[0] == 'E':
            outputString = encrypt_caesar(inputString)
        else:
            outputString = decrypt_caesar(inputString)
    elif cipherType[0] == 'V':
        print("It's a Vigenere cipher!")
        keyword = input('Passkey? ').upper()
        if inputType[0] == 'E':
            outputString = encrypt_vigenere(inputString, keyword)
        else:
            outputString = decrypt_vigenere(inputString, keyword)
    else:
        print("It's a Railfence cipher!")
        railNum = int(input('Number of rails? '))
        if inputType[0] == 'E':
            outputString = encrypt_railfence(inputString, railNum)
        else:
            outputString = decrypt_railfence(inputString, railNum)        

    
    # print('Encrypting' + + 'using' + + 'with' + 'key' + )

    print("*Output*")
    inputType = input('(F)ile or (S)tring? ').upper()  # Print or write the transformed output
    while not inputType or inputType[0] not in ['F','S']:
        inputType = input('(F)ile or (S)tring? ').upper()
    if inputType[0] == 'S':
        inputString = "Here it is!"
        print (outputString)
    else:
        filename = input('Filename? ')
        write_to_file(filename,outputString)
        print ("Finished!")

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
