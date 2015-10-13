"""
Assignment 1: Cryptography
Course: CS 92SI
Name: James Cranston
Date: due 10/9/15 (submitting one day late)

Cryptography program! :)
"""
import string

def get_caesar_dict_encrypt():
    new_alphabet = "XYZ" + string.ascii_uppercase
    caesar_dict = {}

    # map alphabet characters to those shifted three right, wrapping around
    for i in range(len(new_alphabet) - 3):
        caesar_dict[new_alphabet[i]] = new_alphabet[i + 3]

    return caesar_dict

def get_caesar_dict_decrypt():
    new_alphabet = "XYZ" + string.ascii_uppercase
    caesar_dict = {}

    # map alphabet characters to those shifted three left, wrapping around
    for i in range(3, len(new_alphabet)):
        caesar_dict[new_alphabet[i]] = new_alphabet[i - 3]

    return caesar_dict

def encrypt_caesar(plaintext):
    """
    Encrypts plaintext using a Caesar cipher.
    """
    letters = ''.join(filter(str.isalpha, plaintext)).upper()
    caesar_dict = get_caesar_dict_encrypt()

    ciphertext = ""

    # create ciphertext
    for ch in letters:
        ciphertext += caesar_dict[ch]

    return ciphertext


def decrypt_caesar(ciphertext):
    """
    Decrypts a ciphertext using a Caesar cipher.
    """
    letters = ''.join(filter(str.isalpha, ciphertext)).upper()
    caesar_dict = get_caesar_dict_decrypt()

    plaintext = ""

    for ch in letters:
        plaintext += caesar_dict[ch]

    return plaintext

def format_plaintext_keyword(plaintext, keyword):
    """
    Helper for viginere cipher
    """
    plaintext = ''.join(filter(str.isalpha, plaintext)).upper()
    keyword = ''.join(filter(str.isalpha, keyword)).upper()
    return (plaintext, keyword)    

def get_vigenere_key(keyword, plaintext):
    """
    Helper for viginere cipher
    """
    key = keyword
    while len(key) < len(plaintext):
        key += keyword
    key = key[:len(plaintext)]
    return key    

# p, k = 'attack at dawn', '   lemon    '
# 'LX`OPVE`RNbR'

def encrypt_vigenere(plaintext, keyword):
    """
    Encrypts plaintext using a Vigenere cipher with a keyword.
    """
    (plaintext, keyword) = format_plaintext_keyword(plaintext, keyword)

    # builds key
    key = get_vigenere_key(keyword, plaintext)

    ciphertext = ""

    # encrypts the plaintext
    for i in range(len(key)):
        ciphertext += chr(ord(plaintext[i]) + ord(key[i]) - ord('A'))

    return ciphertext


def decrypt_vigenere(ciphertext, keyword):
    """
    Decrypts ciphertext using a Vigenere cipher with a keyword.
    """
    (ciphertext, keyword) = format_plaintext_keyword(ciphertext, keyword)

    # builds key
    key = get_vigenere_key(keyword, ciphertext)

    plaintext = ""

    # decrypts ciphertext
    for i in range(len(key)):
        plaintext += chr(ord(ciphertext[i]) - ord(key[i]) + ord('A'))

    return plaintext


def encrypt_railfence(plaintext, num_rails):
    """
    Encrypts plaintext using a railfence cipher.
    Performs splicing and ciphertext construction in O(num_rails) time.
    """
    letters = ''.join(filter(str.isalpha, plaintext)).upper()
    
    # edge case if num_rails <= 1 just use plaintext
    if num_rails <= 1:
        return letters

    splice_dist = 2 * (num_rails - 1)

    # result string
    ciphertext = ''

    # splice the plaintext and create ciphertext
    for i in range(num_rails):
        # create one list and append to ciphertext
        if i == 0 or i == num_rails - 1:
            ciphertext += ''.join(letters[i::splice_dist])

        # create two alternating lists and alternate append to ciphertext
        else:
            list1 = list(letters[i::splice_dist])
            list2 = list(letters[splice_dist - i::splice_dist])

            # add empty string entries to make lists equal length
            (shorter, longer) = (list1, list2) if len(list1) < len(list2) else (list2, list1)
            for _ in range(0, len(longer) - len(shorter)):
                shorter.append('')

            # append alternating characters from list1, list2
            zipped = zip(list1, list2)
            for (char1, char2) in zipped:
                ciphertext += char1 + char2

    return ciphertext
    

def decrypt_railfence(ciphertext, num_rails):
    """
    Encrypts plaintext using a railfence cipher.
    Add more implementation details here.
    """
    letters = ''.join(filter(str.isalpha, ciphertext)).upper()

    # edge case if num_rails <= 1
    if num_rails <= 1:
        return letters

    # creates two dimensional grid of dimension num_rows * len(ciphertext)
    n = len(letters)
    splice_dist = 2 * (num_rails - 1)
    grid = [['.' for _ in range(n)] for _ in range(num_rails)]
    idx = 0

    # map ciphertext to grid
    for i in range(num_rails):
        for j in range(n):
            if idx >= n:
                break;

            # first and last rails
            if (j - i) % splice_dist == 0:
                grid[i][j] = letters[idx]
                idx += 1

            # middle rails
            if i != 0 and i != num_rails - 1 and (j + i) % splice_dist == 0:
                grid[i][j] = letters[idx]
                idx += 1

    # read plaintext from grid
    direction = 1
    rail = 0
    plaintext = ''

    # read plaintext from grid
    for i in range(n):
        plaintext += grid[rail][i]
        if i != 0 and i % (num_rails - 1) == 0:
            direction *= -1
        rail += direction

    return plaintext


def read_from_file(filename):
    """
    Reads and returns content from a file.
    Add more implementation details here.o
    """
    pass  # woops should have decomposed and did these but I didn't have time to after I finished :(


def write_to_file(filename, content):
    """
    Writes content to a file.
    Add more implementation details here.
    """
    pass  # woops should have decomposed and did these but I didn't have time to after I finished :(


def run_suite():
    """
    Runs a single iteration of the cryptography suite.

    Asks the user for input text from a string or file, whether to encrypt
    or decrypt, what tool to use, and where to show the output.
    """
    # get input format
    print("*Input*")
    input_choice = input("(F)ile or (S)tring? ").upper()
    while not input_choice or input_choice[0] not in ['F', 'S']:
        input_choice = input("Please enter either 'F' for file or 'S' for string. Again (F/S)? ").upper()

    filename = ""
    input_text = ""

    # file input
    if input_choice[0] == "F":
        filename = input("Filename? ")
        while not filename or len(filename) < 1:
            filename = input("Please enter a valid non-empty filename. ")
        with open(filename, "r") as f:
            input_text = f.read().replace("\n", "")
        f.closed

    # string input
    else:
        input_text = input("Enter a string: ")

    # get transformation type
    print("...\n*Transform*")
    transform_choice = input("(E)ncrypt or (D)ecrypt? ").upper()
    while not transform_choice or transform_choice[0] not in ["E", "D"]:
        transform_choice = input("Please enter either 'E' for encrypt or 'D' for decrypt. Again (E/D? ").upper()

    output_text = ""

    # encryption
    if transform_choice[0] == "E":
        encrypt_choice = input("(C)aesar, (V)igenere, or (R)ailfence? ").upper()
        while not encrypt_choice or encrypt_choice[0] not in ["C", "V", "R"]:
            encrypt_choice = input("Plese enter either 'C' for Caesar, 'V' for Viginere, or 'R' for railfence. Again(C/V/R) ").upper()
        method = "Caesar" if encrypt_choice[0] == "C" else "Viginere" if encrypt_choice[0] == "V" else "railfence"

        # Caesar cipher encryption
        if encrypt_choice == "C":
            print("Encrypting '{0}' using {1} cipher".format(input_text, method))
            output_text = encrypt_caesar(input_text)

        # Viginere cipher encryption
        elif encrypt_choice == "V":
            passkey = input("Passkey? ")
            while not passkey or len(passkey) < 1:
                passkey = input("Please enter a valid passkey? ")
            print("Encrypting '{0}' using {1} cipher with key {2}".format(input_text, method, passkey))
            output_text = encrypt_viginere(input_text, passkey)

        # railfence cipher encryption
        else:
            num_rails = int(input("How many (positive integer) rails? "))
            while not num_rails or int(num_rails) < 1:
                num_rails = input("How many (positive integer) rails? ")
            print("Encrypting '{0}' using {1} with {2} rails".format(input_text, method, num_rails))
            output_text = encrypt_railfence(input_text, num_rails)

    # decryption
    else:
        decrypt_choice = input("(C)aesar, (V)igenere, or (R)ailfence? ").upper()
        while not decrypt_choice or decrypt_choice[0] not in ["C", "V", "R"]:
            decrypt_choice = input("Plese enter either 'C' for Caesar, 'V' for Viginere, or 'R' for railfence. Again(C/V/R) ").upper()
        method = "Caesar" if decrypt_choice[0] == "C" else "Viginere" if decrypt_choice[0] == "V" else "railfence"
        source = filename if input_choice == "F" else input_text
        
        # Caesar cipher decryption
        if decrypt_choice == "C":
            print("Decrypting contents of '{0}' using {1} cipher".format(source, method))
            output_text = decrypt_caesar(input_text)

        # Viginere ciphere decryption
        elif decrypt_choice == "V":
            passkey = input("Passkey? ")
            while not passkey or len(passkey) < 1:
                passkey = input("Please enter a valid passkey? ")            
            print("Decrypting contents of '{0}' using {1} cipher with passkey {2}".format(source, method, passkey))
            ouptut_text = decrypt_viginere(input_text, passkey)

        # railcence cipher decryption
        else:
            num_rails = int(input("How many (positive integer) rails? "))
            while not num_rails or num_rails < 1:
                num_rails = input("How many (positive integer) rails? ")            
            print("Decrypting contents of '{0}' using {1} cipher".format(source, method, num_rails))
            output_text = decrypt_railfence(input_text, num_rails)

    # get output format
    print("...\n*Output*")
    output_choice = input("(F)ile or (S)tring? ").upper()
    while not output_choice or output_choice[0] not in ['F', 'S']:
        output_choice = input("Please enter either 'F' for file or 'S' for string. Again (F/S)? ").upper()

    # file output
    if output_choice[0] == "F":
        filename = input("Filename? ")
        print("Writing ciphertext to '{0}'".format(filename))
        while not filename or len(filename) < 1:
            filename = input("Please enter a valid non-empty filename. ")
        with open(filename, "w") as output_file:
            output_file.write(output_text)

    # string output
    else:
        print("The output is is: {0}".format(output_text))
    

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
    # run_suite()
    # while should_continue():
    #     run_suite()
    print("Goodbye!")


if __name__ == '__main__':
    """This block is run if and only if the Python script is invoked from the
    command line."""
    main()
