"""
Assignment 1: Cryptography
Course: CS 92SI
Name: Anna Wang
Date: 10/2/15

This program receives text and input from the user to decrypt or encrypt the input text.
"""

def encrypt_caesar(plaintext):
    """
    Encrypts plaintext using a Caesar cipher.
    Add more implementation details here.
    """
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g','h', 'i', 'j', 'k', 'l', 'm','n',
    'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    length = len(letters)
    encryption_lower_case = {val:letters[(index+3)%length] for index, val in enumerate(letters)}
    letters = [v.upper() for v in letters]
    encryption_upper_case = {val:letters[(index+3)%length] for index, val in enumerate(letters)}
    merged_dictionaries = encryption_lower_case.copy()
    merged_dictionaries.update(encryption_upper_case)
    return "".join(merged_dictionaries[letter] for letter in plaintext)

def decrypt_caesar(ciphertext):
    """
    Decrypts a ciphertext using a Caesar cipher.
    Add more implementation details here.
    """
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g','h', 'i', 'j', 'k', 'l', 'm','n',
    'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    length = len(letters)
    encryption_lower_case = {val:letters[(index+26-3)%length] for index, val in enumerate(letters)}
    letters = [v.upper() for v in letters]
    encryption_upper_case = {val:letters[(index+26-3)%length] for index, val in enumerate(letters)}
    merged_dictionaries = encryption_lower_case.copy()
    merged_dictionaries.update(encryption_upper_case)
    return "".join(merged_dictionaries[letter] for letter in ciphertext)

def encrypt_vigenere(plaintext, keyword):
    """
    Encrypts plaintext using a Vigenere cipher with a keyword.
    Add more implementation details here.
    """
    plaintext_len = len(plaintext)
    keyword_len = len(keyword)
    multiplier = plaintext_len / keyword_len
    remainder = plaintext_len % int(keyword_len)
    keyword_compare = keyword * int(multiplier);
    for x in range(0, remainder):
        keyword_compare += keyword[x]
    encrypted_word = ""
    for index, letter in enumerate(plaintext):
        plaintext_char_number = ord(letter.lower()) - ord('a')
        keyword_char_number = ord(keyword_compare[index].lower()) - ord('a')
        int_sum = (plaintext_char_number + keyword_char_number) % 26
        new_letter = chr(int_sum + ord('a'))
        encrypted_word += new_letter
    return encrypted_word

def decrypt_vigenere(ciphertext, keyword):
    """
    Decrypts ciphertext using a Vigenere cipher with a keyword.
    Add more implementation details here.
    """
    ciphertext_len = len(ciphertext)
    keyword_len = len(keyword)
    multiplier = ciphertext_len / keyword_len
    remainder = ciphertext_len % int(keyword_len)
    keyword_compare = keyword * int(multiplier);
    for x in range(0, remainder):
        keyword_compare += keyword[x]
    decrypted_word = ""
    for index, letter in enumerate(ciphertext):
        plaintext_char_number = ord(letter.lower()) - ord('a')
        keyword_char_number = ord(keyword_compare[index].lower()) - ord('a')
        int_sum = (plaintext_char_number - keyword_char_number + 26) % 26
        new_letter = chr(int_sum + ord('a'))
        decrypted_word += new_letter
    return decrypted_word

def fill_rails_with_word(word, num_rails):
    """
    Creates empty railfence with the supplied number of num_rails 
    and fills the fences with the letters of word in vertical order
    """
    lists = [""] * num_rails
    current_rail = 0
    goingDown = True
    for letter in word:
        lists[current_rail] += letter
        if goingDown:
            if current_rail == num_rails - 1:
                current_rail -= 1
                goingDown = False
            else:
                current_rail += 1
        else:
            if current_rail == 0:
                current_rail += 1
                goingDown = True
            else:
                current_rail -= 1
    return lists

def encrypt_railfence(plaintext, num_rails):
    """
    Encrypts plaintext using a railfence cipher.
    Add more implementation details here.
    """
    lists = fill_rails_with_word(plaintext, num_rails)
    return ''.join(word for word in lists)

def decrypt_railfence(ciphertext, num_rails):
    """
    Encrypts plaintext using a railfence cipher.
    Add more implementation details here.
    """
    dashes = "-"*len(ciphertext)
    lists = fill_rails_with_word(dashes, num_rails)

    index_letter = 0
    for index, l in enumerate(lists):
        number_letters = len(l)
        word = ciphertext[index_letter:index_letter + number_letters]
        lists[index] = word
        index_letter += number_letters

    decrypted_word = ""
    current_rail = 0
    goingDown = True
    for index, letter in enumerate(ciphertext):
        decrypted_word += lists[current_rail][:1]
        lists[current_rail] = lists[current_rail][1:]
        if goingDown:
            if current_rail == num_rails - 1:
                current_rail -= 1
                goingDown = False
            else:
                current_rail += 1
        else:
            if current_rail == 0:
                current_rail += 1
                goingDown = True
            else:
                current_rail -= 1
    return decrypted_word
    
def read_from_file(filename):
    """
    Reads and returns content from a file.
    Add more implementation details here.
    """
    with open(filename, 'r') as f:
        return f.read()


def write_to_file(filename, content):
    """
    Writes content to a file.
    Add more implementation details here.
    """
    with open(filename, 'w') as f:
        return f.write(content)

def get_file_or_string():
    """
    Asks user for whether they want file or string,
    and continually prompts the user until they provide valid input
    """
    file_or_string = input("(F)ile or (S)tring? ").upper()
    while file_or_string != 'S' and file_or_string != 'F':
        file_or_string = input("(F)ile or (S)tring? ").upper()
    return file_or_string

def get_encrypt_or_decrypt():
    """
    Asks user for whether they want to encrypt or decrypt,
    and continually prompts the user until they provide valid input
    """
    encrypt_or_decrypt = input("(E)ncrypt or (D)ecrypt? ").upper()
    while encrypt_or_decrypt != 'E' and encrypt_or_decrypt != 'D':
        encrypt_or_decrypt = input("(E)ncrypt or (D)ecrypt? ").upper()
    if encrypt_or_decrypt == "E":
        return "Encrypting"
    else:
        return "Decrypting"

def get_encryption_type():
    """
    Asks user for what kind of cipher they wish to use,
    and continually prompts the user until they provide valid input
    """
    encryption_type = input("(C)aesar, (V)igenere, or (R)ailfence? ").upper()
    while encryption_type != 'C' and encryption_type != 'V' and encryption_type != 'R':
        encryption_type = input("(C)aesar, (V)igenere, or (R)ailfence? ").upper()
    if encryption_type == 'V':
        return "Vigenere"
    elif encryption_type == "R":
        return "Railfence"
    else:
        return "Caesar"

def run_suite():
    """
    Runs a single iteration of the cryptography suite.

    Asks the user for input text from a string or file, whether to encrypt
    or decrypt, what tool to use, and where to show the output.
    """
    print("*Input*")
    file_or_string = get_file_or_string()

    if file_or_string == 'S':
        string = input("Enter the string to encrypt: ")
    else:
        file_name = input("Filename: ")
        string = read_from_file(file_name)

    string = ''.join(c for c in string if c.isalpha())

    print("*Transform*")
    encrypt_or_decrypt = get_encrypt_or_decrypt()
    encryption_type = get_encryption_type()
    morphed_string = ""

    if encryption_type == 'Vigenere':
        passkey = input("Passkey? ")
        if encrypt_or_decrypt == 'Encrypting':
            morphed_string = encrypt_vigenere(string, passkey)
        else:
            morphed_string = decrypt_vigenere(string, passkey)
        print("{type} {input} using Vigenere cipher with key {key}".format(type = encrypt_or_decrypt, input = string, key = passkey))
    elif encryption_type == 'Railfence':
        num_rails = int(input("Number of rails? "))
        if encrypt_or_decrypt == 'Encrypting':
            morphed_string = encrypt_railfence(string, num_rails)
        else:
            morphed_string = decrypt_railfence(string, num_rails)
        print("{type} {input} using Railfence cipher with {num} rails".format(type = encrypt_or_decrypt, input = string, num = num_rails))
    else:
        if encrypt_or_decrypt == 'Encrypting':
            morphed_string = encrypt_caesar(string)
        else:
            morphed_string = decrypt_caesar(string)
        print("{type} {input} using Caesar cipher".format(type = encrypt_or_decrypt, input = string))

    print("*Output*")
    file_or_string = get_file_or_string()
    if file_or_string == 'S':
        print("The plaintext is {string}".format(string = morphed_string))
    else:
        file_name = input("Filename: ")
        write_to_file(file_name, morphed_string)

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
