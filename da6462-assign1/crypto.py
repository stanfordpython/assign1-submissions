"""
Assignment 1: Cryptography
Course: CS 92SI
Name: <YOUR NAME>
Date: <DATE>

Replace this with a description of the program.
"""

def encrypt_caesar(plaintext):
    """
    Encrypts plaintext using a Caesar cipher.
    Add more implementation details here.
    """
    encrypt = []
    for i in plaintext.upper():
        c = ord(i) + 3
        if c > 90:
            encrypt.append(chr(c - 26))
        else:
            encrypt.append(chr(c))
    return "".join(encrypt)

def decrypt_caesar(ciphertext):
    """
    Decrypts a ciphertext using a Caesar cipher.
    Add more implementation details here.
    """
    decrypt = []
    for i in ciphertext.upper():
        c = ord(i) - 3
        if c < 65:
            decrypt.append(chr(c + 26))
        else:
            decrypt.append(chr(c))
    return "".join(decrypt)

def encrypt_vigenere(plaintext, keyword):
    """
    Encrypts plaintext using a Vigenere cipher with a keyword.
    Add more implementation details here.
    """
    keyword = (keyword *((len(plaintext) / len(keyword)) + 1)).upper()
    keyword = keyword[: len(plaintext)]
    final = []
    for i, c in enumerate(plaintext.upper()):
        letter = ord(c) + ord(keyword[i])
        while letter > 90 or letter < 65:
            temp = letter % 91
            temp = letter % 26
            letter = 65 + temp
        final.append(chr(letter))
    return "".join(final)

def decrypt_vigenere(ciphertext, keyword):
    """
    Decrypts ciphertext using a Vigenere cipher with a keyword.
    Add more implementation details here.
    """
    keyword = (keyword *((len(ciphertext) / len(keyword)) + 1)).upper()
    keyword = keyword[: len(ciphertext)]
    final = []
    for i, c in enumerate(ciphertext.upper()):
        letter = ord(c) - ord(keyword[i])
        while letter > 90 or letter < 65:
            temp = letter % 91
            temp = letter % 26
            letter = 65 + temp
        final.append(chr(letter))
    return "".join(final)

def encrypt_railfence(plaintext, num_rails):
    """
    Encrypts plaintext using a railfence cipher.
    Add more implementation details here.
    """
    total_chr = len(plaintext)
    direction = 1
    zig_zag = [""] *num_rails
    rail = 0
    i = 0
    while total_chr > 0:
        zig_zag[rail] += plaintext[i]
        total_chr -= 1
        if rail == num_rails - 1 and direction == 1:
            direction *= -1
        if rail == 0 and direction == -1:
            direction *= -1
        rail += direction
        i += 1
    return "".join(zig_zag)

def decrypt_railfence(ciphertext, num_rails):
    """
    Encrypts plaintext using a railfence cipher.
    Add more implementation details here.
    """
    if num_rails == 1:
        return ciphertext
    l = []
    num_segments = len(ciphertext) / (num_rails - 1)
    last_segment = len(ciphertext) % (num_rails - 1)
    if last_segment == 0:
        total_segment = num_segments
    else:
        total_segment = num_segments + 1

    num_per_rail = [0] * num_rails

    #num_per_rail gives you the number of characters per rail

    for i in range(1, total_segment+1):
        if i % 2 != 0:
            num_per_rail[0] += 1
    num_per_rail[-1] = total_segment - num_per_rail[0]

    for i in range(1, num_rails - 1):
        num_per_rail[i] = (len(ciphertext) - num_per_rail[-1] - num_per_rail[0]) / (num_rails - 2)
    if last_segment != 0:
        extra = (len(ciphertext) - num_per_rail[-1] - num_per_rail[0]) % (num_rails - 2)
        if total_segment % 2 == 0:
            for i in range(num_rails - 2, 0, -1):
                if extra > 0:
                    num_per_rail[i] += 1
                    extra -= 1
        else:
            for i in range(1, num_rails - 1):
                if extra > 0:
                    num_per_rail[i] += 1
                    extra -= 1
    total_chr = len(ciphertext)
    direction = 1
    curr_rail = 0
    curr_index = 0
    while total_chr > 0:
        l.append(ciphertext[curr_index])
        total_chr -= 1
        if curr_rail == num_rails - 1 and direction == 1:
            direction *= -1
            num_per_rail[-2] -= 1
        if curr_rail == 0 and direction == -1:
            direction *= -1
            num_per_rail[0] += 1

        if direction == 1:
            curr_index += num_per_rail[curr_rail]
        else:
            curr_index -= num_per_rail[curr_rail - 1]
        curr_rail += direction
    return "".join(l)

def read_from_file(filename):
    """
    Reads and returns content from a file.
    Add more implementation details here.
    """
    f = open(filename, 'r')
    return f.read()


def write_to_file(filename, content):
    """
    Writes content to a file.
    Add more implementation details here.
    """
    f = open(filename, 'w')
    f.write(content)


def strip_string(usr_input):
    '''
    Strips all non-alphabetic characters and returns
    new string
    '''
    return "".join([i for i in usr_input.upper() if ord(i) < 91 and ord(i) > 64])


def run_suite():
    """
    Runs a single iteration of the cryptography suite.

    Asks the user for input text from a string or file, whether to encrypt
    or decrypt, what tool to use, and where to show the output.
    """
    print("*Input*")
    a = input("(F)ile or (S)tring? ").upper()
    while not a or a[0] not in ['F', 'S']:
        a = input("Please enter either (F)ile or (S)tring ")
    if a == "F":
        fn = input("Filename: ")
        usr_input = strip_string(read_from_file(fn))
    else:
        usr_input = strip_string(input("Enter the string to encrypt: "))

    print("*Transform*")
    b = input("(E)ncrpyt or (D)ecrpyt? ").upper()
    while not b or b not in ['E', 'D']:
        b = input("Please enter either (E)ncrypt or (D)ecrypt")
    c = input("(C)aesar, (V)igenere, or (R)ailfence? ").upper()
    while not c or c not in ['C', 'V', 'R']:
        c = input("Please enter either (C)aesar, (V)igenere, or (R)ailfence")

    if c == "C":
        if b == 'E':
            final_output = encrypt_caesar(usr_input)
        else:
            final_output = decrypt_caesar(usr_input)
    elif c == "V":
        if b == 'E':
            key = input("Passkey? ")
            final_output = encrypt_vigenere(usr_input, key)
        else:
            key = input("Passkey? ")
            final_output = decrypt_vigenere(usr_input, key)
    else:
        if b == 'E':
            rails = input('Number of rails? ')
            final_output = encrypt_railfence(usr_input, rails)
        else:
            rails = input('Number of rails? ')
            final_output = decrypt_railfence(usr_input, rails)
    print("*Output*")
    d = input("(F)ile or (S)tring? ").upper()
    while not d or d[0] not in ['F', 'S']:
        d = input("Please enter either (F)ile or (S)tring ")
    if d == "S":
        print final_output
    else:
        fn = input("Enter the file name")
        write_to_file(fn, final_output)

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
