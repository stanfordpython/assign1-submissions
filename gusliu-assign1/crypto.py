"""
Assignment 1: Cryptography
Course: CS 92SI
Name: <Gus Liu>
Date: <10/7/15>

Replace this with a description of the program.
"""

def encrypt_caesar(plaintext):
    """
    Encrypts plaintext using a Caesar cipher.
    Add more implementation details here.
    """
    encrypted = ''
    for char in plaintext:
        ascii = ord(char) + 3
        if char.isupper():
            ascii -= ord('A')
            ascii %= 26
            encrypted += chr(ord('A') + ascii)
        else:
            ascii -= ord('a')
            ascii %= 26
            encrypted += chr(ord('a') + ascii)
    return encrypted


def decrypt_caesar(ciphertext):
    """
    Decrypts a ciphertext using a Caesar cipher.
    Add more implementation details here.
    """
    encrypted = ''
    for char in ciphertext:
        ascii = ord(char) - 3
        if char.isupper():
            ascii -= ord('A')
            if ascii < 0:
                ascii += 26
            encrypted += chr(ord('A') + ascii)
        else:
            ascii -= ord('a')
            if ascii < 0:
                ascii += 26
            encrypted += chr(ord('a') + ascii)
    return encrypted

def get_vigenere_key(length, keyword):
    repeats = length // len(keyword)
    leftover = length % len(keyword)
    key = keyword * repeats + keyword[:leftover]
    return key

def encrypt_vigenere(plaintext, keyword):
    """
    Encrypts plaintext using a Vigenere cipher with a keyword.
    Add more implementation details here.
    """
    plaintext = plaintext.upper()
    keyword = keyword.upper()
    length = len(plaintext)
    key = get_vigenere_key(length, keyword)
    encrypted = ''
    for i in range(length):
        pchar = plaintext[i]
        kchar = key[i]
        ascii = (ord(pchar) + ord(kchar)) % 26
        encrypted += chr(ord('A') + ascii)
    return encrypted



def decrypt_vigenere(ciphertext, keyword):
    """
    Decrypts ciphertext using a Vigenere cipher with a keyword.
    Add more implementation details here.
    """
    ciphertext = ciphertext.upper()
    length = len(ciphertext)
    key = get_vigenere_key(length, keyword)
    decrypted = ''
    for i in range(length):
        cchar = ciphertext[i]
        kchar = key[i]
        ascii = (ord(cchar) - ord(kchar)) % 26
        decrypted += chr(ord('A') + ascii)
    return decrypted


def encrypt_railfence(plaintext, num_rails):
    """
    Encrypts plaintext using a railfence cipher.
    Add more implementation details here.
    """
    rows = [''] * num_rails
    length = len(plaintext)
    for i in range(length):
        n = i // (num_rails - 1)
        index = i % (num_rails - 1)
        if n % 2 != 0:
            index = num_rails - 1 - index
        rows[index] += plaintext[i]
    z = [''.join(x) for x in rows]
    return ''.join(z)


def decrypt_railfence(ciphertext, num_rails):
    """
    Encrypts plaintext using a railfence cipher.
    Add more implementation details here.
    """
    lengths = [0] * num_rails
    rows = [''] * num_rails
    length = len(ciphertext)
    row = 0
    going_down = True
    for i in range(length):
        if row == 0:
            going_down = True
        if row == num_rails - 1:
            going_down = False
        lengths[row] += 1
        if going_down:
            row += 1
        else:
            row -= 1
    index = 0
    for i in range(num_rails):
        rows[i] = ciphertext[index:index + lengths[i]]
        index += lengths[i]
    going_down = True
    encrypted = ''
    row = 0
    for i in range(length):
        if row == 0:
            going_down = True
        if row == num_rails - 1:
            going_down = False
        encrypted += (rows[row])[0]
        rows[row] = (rows[row])[1:]
        if going_down:
            row += 1
        else:
            row -= 1
    return encrypted    


def read_from_file(filename):
    """
    Reads and returns content from a file.
    Add more implementation details here.
    """
    with open(filename, 'r') as f:
        content = f.read()
    f.closed
    return content


def write_to_file(filename, content):
    """
    Writes content to a file.
    Add more implementation details here.
    """
    with open(filename, 'w') as f:
        f.write(content)
    f.close()


def run_suite():
    """
    Runs a single iteration of the cryptography suite.

    Asks the user for input text from a string or file, whether to encrypt
    or decrypt, what tool to use, and where to show the output.
    """
    print("*Input*")
    input_type = input('(F)ile or (S)tring? ').lower()
    while True:
        if input_type == 's':
            s = input('Enter the string to encrypt: ').lower()
        elif input_type == 'f':
            file_name = input('Filename? ')
            s = read_from_file(file_name).lower()
        else:
            continue
        break

    s = s.replace(" ", "")

    print("*Transform*")
    transform_type = input('(E)ncrypt or (D)ecrypt? ').lower()
    while transform_type != 'e' and transform_type != 'd':
        transform_type = input('(E)ncrypt or (D)ecrypt? ').lower()

    transform_method = input('(C)aesar, (V)igenere, or (R)ailfence? ').lower()
    while transform_method != 'c' and transform_method != 'v' and transform_method != 'r':
        transform_method = input('(C)aesar, (V)igenere, or (R)ailfence? ').lower()

    if transform_method == 'c':
        if transform_type == 'e':
            print("Encrypting " + s + " using Caesar cipher...")
            output = encrypt_caesar(s)
        else:
            print("Decrypting " + s + " using Caesar cipher...")
            output = decrypt_caesar(s)
    elif transform_method == 'v':
        secret_key = input('Passkey? ')
        if transform_type == 'e':
            print("Encrypting " + s + " using Vigenere cipher with key " + secret_key + "...")
            output = encrypt_vigenere(s, secret_key)
        else:
            print("Decrypting " + s + " using Vigenere cipher with key " + secret_key + "...")
            output = decrypt_vigenere(s, secret_key)
    elif transform_method == 'r':
        num_rails = input('Number of rails? ')
        while not num_rails.isnumeric():
            num_rails = input('Number of rails? ')
        num_rails = int(num_rails)
        if transform_type == 'e':
            print("Encrypting " + s + " using railfence cipher with " + num_rails + " rails...")
            output = encrypt_railfence(s, num_rails)
        else:
            print("Decrypting " + s + " using railfence cipher with " + num_rails + " rails...")
            output = decrypt_railfence(s, num_rails)

    print("*Output*")
    output_type = input('(F)ile or (S)tring? ').lower()
    while True:
        if output_type == 's':
            print(output)
        elif output_type == 'f':
            file_name = input('Filename? ')
            print("Writing ciphertext to " + file_name)
            write_to_file(file_name, output)
        else:
            continue
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
