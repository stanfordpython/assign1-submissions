"""
Assignment 1: Cryptography
Course: CS 92SI
Name: Jean-Luc Watson
Date: October 9th, 2015 

Three-function cryptography suite: implements Caesar, Vigenere, and Railfence
encryption and decryption, as well as a text-based user interface for repeated use.
"""
import math

# base for character shifts
ascii_base = ord('A')
# map comprehension for caesar cipher character encryption 
caesar_encryption_mapping = {chr(c): chr(ascii_base + ((c - ascii_base + 3) % 26)) for c in range(ascii_base, ascii_base + 26)}
# map comprehension for caesar cipher character decryption
caesar_decryption_mapping = {chr(c): chr(ascii_base + ((c - ascii_base - 3) % 26)) for c in range(ascii_base, ascii_base + 26)}


def encrypt_caesar(plaintext):
    """
    Encrypts plaintext using a Caesar cipher.
    Uses the precomputed plain -> encrypted character map to calculate each character
    of the resulting ciphertext 
    """
    ciphertext = ""
    for char in plaintext.upper():
        ciphertext += caesar_encryption_mapping[char] 
    return ciphertext


def decrypt_caesar(ciphertext):
    """
    Decrypts a ciphertext using a Caesar cipher.
    Uses the precomputed encrypted -> plain character map to calculate each character
    of the resulting plaintext
    """
    plaintext = ""
    for char in ciphertext.upper():
        plaintext += caesar_decryption_mapping[char]
    return plaintext


def encrypt_vigenere(plaintext, keyword):
    """
    Encrypts plaintext using a Vigenere cipher with a keyword.
    Generates the length-matching keyword with the appropriate list slice and shifts
    the characters by total sum of the keyword character and the plaintext character
    at a specific index (e.g. A -> B if the total sum is 1). The characters wrap around
    if too large. 
    """

    plaintext = plaintext.upper()
    keyword = keyword.upper()
    matching_length_key = (keyword * math.ceil(len(plaintext) / len(keyword)))[:len(plaintext)]

    ciphertext = ""
    for index, char in enumerate(plaintext):
        total_value = (ord(char) - ascii_base) + (ord(matching_length_key[index]) - ascii_base)
        ciphertext += chr(ascii_base + (total_value % 26))
    return ciphertext


def decrypt_vigenere(ciphertext, keyword):
    """
    Decrypts ciphertext using a Vigenere cipher with a keyword.
    Generates the corresponding plaintext using the exact opposite process as that used above,
    subtracting the total key value from the character value to reverse the process. 
    """
    ciphertext = ciphertext.upper()
    keyword = keyword.upper()
    matching_length_key = (keyword * math.ceil(len(ciphertext) / len(keyword)))[:len(ciphertext)]

    plaintext = ""
    for index, char in enumerate(ciphertext):
        total_value = (ord(char) - ascii_base) - (ord(matching_length_key[index]) - ascii_base)
        plaintext += chr(ascii_base + (total_value % 26))
    return plaintext


def num_letters_in_rail(text, rail, num_rails):
    """
    Calculates the number of letters in a specific rail index for the railfence cipher.
    Allocates one character per 'up' or 'down' sequence of characters to each of the
    intermediary rails and half of that number to the first and last rails. Then distributes
    the extra characters at the end of the string to the appropriate rails. 
    """

    num_segments = len(text) // (num_rails - 1)
    if rail == 0:
        letters_in_rail = math.ceil(num_segments / 2)
    elif rail == num_rails - 1:
        letters_in_rail = num_segments // 2
    else:
        letters_in_rail = num_segments

    extra_letters = len(text) % (num_rails - 1)
    if extra_letters != 0 and ((num_segments % 2 == 0 and rail < extra_letters) or \
                               (num_segments % 2 == 1 and rail >= num_rails - extra_letters)):
       letters_in_rail += 1
    return letters_in_rail


def encrypt_railfence(plaintext, num_rails):
    """
    Encrypts plaintext using a railfence cipher.
    For the first and last rail, takes a slice of the plaintext of characters every
    (n_rails -1)*2 indices. For each of the intermediate rails, the width of the slice
    is the same, but two slices must be made and interwoven to create the complete
    representation of the rail
    """
    if num_rails == 1:
        return plaintext

    ciphertext = ""
    for r in range(num_rails):

        rail = [None] * num_letters_in_rail(plaintext, r, num_rails)
        if r > 0 and r < num_rails - 1: # not the last rail or the first one
            rail[::2] = plaintext[r::(num_rails - 1)*2]
            rail[1::2] = plaintext[r + (num_rails - r - 1)*2::(num_rails - 1)*2]
        else:
            rail[::] = plaintext[r::(num_rails - 1)*2]

        ciphertext += "".join(rail)

    return ciphertext


def decrypt_railfence(ciphertext, num_rails):
    """
    Decrypts ciphertext using a railfence cipher.
    Calculates the length of each rail, and assigns the slice of the ciphertext representing
    the rail to be staggered by (num_rails-1)*2 indices in the plaintext. Does two passes
    over intermediary rails and one over the first and last rails.
    """
    if num_rails == 1:
        return ciphertext

    plaintext_arr = [None] * len(ciphertext)
    cipher_index = 0

    for r in range(num_rails):
        num_letters = num_letters_in_rail(ciphertext, r, num_rails)
        if r  > 0 and r < num_rails - 1:
            plaintext_arr[r::(num_rails - 1)*2] = ciphertext[cipher_index:cipher_index+num_letters:2]
            plaintext_arr[r + (num_rails - r - 1)*2::(num_rails - 1)*2] = ciphertext[cipher_index + 1:cipher_index+num_letters:2]
        else:
            plaintext_arr[r::(num_rails - 1)*2] = ciphertext[cipher_index:cipher_index+num_letters]

        cipher_index += num_letters

    return "".join(plaintext_arr)


def read_from_file(filename):
    """
    Reads and returns content from a file.
    Combines all lines, strips all non-alpha characters, and uppercases all characters.
    Returns the parsed contents of the file in one string.
    """
    with open(filename, 'r') as f:
        lines = f.readlines()
        return strip_nonalpha("".join(lines)).upper()


def write_to_file(filename, content):
    """
    Writes content to a file.
    The content is written as is to the file. 
    """
    with open(filename, 'w') as f:
        f.write(content)


def strip_nonalpha(str):
    """
    Strips all non-alpha characters from the given string
    """
    return "".join([c for c in str if c.isalpha()])


def run_crypto_algorithm(encrypt, text, filename):
    """
    Prompts the user to run a specific cryptography algorithm, one of Caesar, Vigenere, or Railfence.
    Reprompts until it receives valid input.
    param encrypt: Boolean, indicates whether to encrypt or decrypt the input
    param text: input value to be encrypted/decrypted
    param filename: if the input was read from a file, the filename is given
    """
    while True:
        encryption_type = strip_nonalpha(input("(C)aesar, (V)igenere, or (R)ailfence? ")).upper()
        if encryption_type == "C":
            return run_caesar(encrypt, text, filename)
        elif encryption_type == "V":
            return run_vigenere(encrypt, text, filename)
        elif encryption_type == "R":
            return run_railfence(encrypt, text, filename)


def run_caesar(encrypt, text, filename):
    """
    Runs either caesar encryption or decryption on the input text for the suite
    """
    if encrypt:
        if filename:
            print("Encrypting contents of "+filename+" using Caesar cipher")
        else:
            print("Encrypting "+text+" using Caesar cipher")
        print("...")
        return encrypt_caesar(text)
    else:
        if filename:
            print("Decrypting contents of "+filename+" using Caesar cipher")
        else:
            print("Decrypting "+text+" using Caesar cipher")
        print("...")
        return decrypt_caesar(text)


def run_vigenere(encrypt, text, filename):
    """
    Runs either Vigenere encryption or decryption on the input text. Also asks the user for a valid
    passkey, which is stripped of non-alpha and uppercased.
    """

    passkey = strip_nonalpha(input("Passkey? ")).upper()
    if encrypt:
        if filename:
            print("Encrypting contents of "+filename+" using Vigenere cipher with key "+passkey)
        else:
            print("Encrypting "+text+" using Vigenere cipher with key "+passkey)
        print("...")
        return encrypt_vigenere(text, passkey)
    else:
        if filename:
            print("Decrypting contents of "+filename+" using Vigenere cipher with key "+passkey)
        else:
            print("Decrypting "+text+" using Vigenere cipher with key "+passkey)
        print("...")
        return decrypt_vigenere(text, passkey)


def run_railfence(encrypt, text, filename):
    """
    Runs either railfence encryption or decyrption on the input text. Also asks the user for a valid
    positive number of rails.
    """
    
    num_rails = int(input("Positive number of rails? "))
    if encrypt:
        if filename:
            print("Encrypting contents of "+filename+" using Railfence cipher with "+str(num_rails)+" rails")
        else:
            print("Encrypting "+text+" using Railfence cipher with "+str(num_rails)+" rails")
        print("...")
        return encrypt_railfence(text, num_rails)
    else:
        if filename:
            print("Decrypting contents of "+filename+" using Railfence cipher with "+str(num_rails)+" rails")
        else:
            print("Decrypting "+text+" using Railfence cipher with "+str(num_rails)+" rails")
        print("...")
        return decrypt_railfence(text, num_rails)


def run_suite():
    """
    Runs a single iteration of the cryptography suite.

    Asks the user for input text from a string or file, whether to encrypt
    or decrypt, what tool to use, and where to show the output.
    """
    while True:
        print("*Input*")
        filename = ""
        while True:
            option = strip_nonalpha(input("(F)ile or (S)tring? ")).upper()
            if option == "F":
                filename = input("Filename? ")
                input_text = read_from_file(filename)
                inputIsFile = True
                break
            elif option == "S":
                input_text = strip_nonalpha(input("Enter the string to encrypt: ")).upper()
                break

        print("*Transform*")
        while True:
            option = strip_nonalpha(input("(E)ncrypt or (D)ecrypt? ")).upper()
            if option == "E" or option == "D":
                output_text = run_crypto_algorithm(option == "E", input_text, filename)
                break

        print("*Output*")
        while True:
            option = strip_nonalpha(input("(F)ile or (S)tring? ")).upper()
            if option == "F":
                filename = input("Filename? ")
                print("Writing ciphertext to "+filename+"...")
                write_to_file(filename, output_text)
                break
            elif option == "S":
                print("The plaintext is:", output_text)
                break

        again = strip_nonalpha(input("Again (Y/N)? ")).upper()
        if again == "N":
            break


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
