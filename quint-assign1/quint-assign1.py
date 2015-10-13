"""
Assignment 1: Cryptography
Course: CS 92SI
Name: Quint Underwood
Date: 9 October 2015

Replace this with a description of the program.
"""

def encrypt_caesar(plaintext):
    """
    Encrypts plaintext using a Caesar cipher.
    Add more implementation details here.
    """
    shift = int(input("By how many letters do you want to shift? "))
    encoded_phrase = ""
    for letter in plaintext:
        letter = chr(ord(letter) + shift)
        if letter > 'z':
            letter = chr(ord(letter) - 26)
        encoded_phrase += letter
    #print(encoded_phrase.upper())
    return(encoded_phrase.upper())


def decrypt_caesar(ciphertext):
    """
    Decrypts a ciphertext using a Caesar cipher.
    Add more implementation details here.
    """
    shift = int(input("How many letters was this phrase shifted when it was encoded? "))
    decoded_phrase = ""
    for letter in ciphertext:
        letter = chr(ord(letter) - shift)
        if letter < 'a':
            letter = chr(ord(letter) + 26)
        decoded_phrase += letter
    return(decoded_phrase.upper())

def encrypt_vigenere(plaintext, keyword):
    """
    Encrypts plaintext using a Vigenere cipher with a keyword.
    Add more implementation details here.
    """
    encoded_phrase = ""
    length = len(keyword)
    i=0
    for letter in plaintext:
        letter = chr(ord(letter) + ord(keyword[i%length]) - ord('a'))
        if letter > 'z':
            letter = chr(ord(letter) - 26)
        encoded_phrase += letter
        i += 1
    return (encoded_phrase)



def decrypt_vigenere(ciphertext, keyword):
    """
    Decrypts ciphertext using a Vigenere cipher with a keyword.
    Add more implementation details here.
    """
    decoded_phrase = ""
    length = len(keyword)
    i=0
    for letter in ciphertext:
        letter = chr(ord(letter) - ord(keyword[i%length]) + ord('a'))
        if letter < 'a':
            letter = chr(ord(letter) + 26)
        decoded_phrase += letter
        i += 1
    return (decoded_phrase)


def encrypt_railfence(plaintext, num_rails):
    """
    Encrypts plaintext using a railfence cipher.
    Add more implementation details here.
    """
    divisor = 2 * num_rails - 2
    encoded_phrase = ""
    rails = [[letter for n, letter in enumerate(plaintext) if ((n+i) % divisor == 0 or (n-i) % divisor == 0)] for i in range(num_rails)]
    for rail in rails:
        for element in rail:
            encoded_phrase += element
    return(encoded_phrase)

def decrypt_railfence(ciphertext, num_rails):
    """
    Encrypts plaintext using a railfence cipher.
    Add more implementation details here.
    """
    
    divisor = 2 * num_rails - 2
    print("divisor= ", divisor)
    length = len(ciphertext)
    decoded_phrase = [None]*length
    print(decoded_phrase)
    print ("ciphertext length=", length)
    rail_length = [length//divisor + 1 if (i < (num_rails - 1) and i > 0) else (length//divisor) for i in range(num_rails)]

    print (rail_length)

    for i in range(length % divisor):
        if i < num_rails - 1:
            rail_length[i] += 1
        else:
            rail_length[num_rails-1 - (i % (divisor//2))] += 1

    print (rail_length)

    n=0
    for i in range(num_rails):
        decoded_phrase[i]=ciphertext[n]
        n+=1
        print("i loop n: ",n)
        for j in range(rail_length[i]-2):
            print("small", (j+1)*divisor-i)
            print("j loop n: ", n)
            decoded_phrase[(j+1)*divisor-i] = ciphertext[n]
            if (j+1)*divisor+1 < len(ciphertext)-1:
                print("big", (j+1)*divisor+1)
                decoded_phrase[(j+1)*divisor+i] = ciphertext[n+1]
                n+=1
                print("if loop n: ",n)
            n+=1
    return(decoded_phrase)
    


def read_from_file(filename):
    """
    Reads and returns content from a file.
    Add more implementation details here.
    """
    pass  # Your implementation here
    


def write_to_file(filename, content):
    """
    Writes content to a file.
    Add more implementation details here.
    """
    pass  # Your implementation here


def run_suite():
    """
    Runs a single iteration of the cryptography suite.

    Asks the user for input text from a string or file, whether to encrypt
    or decrypt, what tool to use, and where to show the output.
    """
    print("*Input*")
    input_method = input("(F)ile or (S)tring? ")
    if input_method == 'S' or 's':
        text = input("Enter the string to encrypt/decrypt: ").lower()
    elif input_method == 'F' or 'f':
        file_path = input("Please enter a file name: ")
        with open(file_path, 'r') as f:
            text = f.read()
    else:
        print("You did not enter in a correct input method.")

    print("*Transform*")
    direction = input("(E)ncrypt or (D)ecrypt? ").upper()
    encrypt_type = input("(C)aesar, (V)igenere, or (R)ailfence? ").upper()

    print("*Output*")
    if direction == 'E':
        if encrypt_type == 'C':
            print(encrypt_caesar(text))
        elif encrypt_type == 'V':
            passkey = input("Passkey? ")
            print(encrypt_vigenere(text, passkey))
        else:
            num_rails = int(input("Number of rails? "))
            print(encrypt_railfence(text, num_rails))
    else:
        if encrypt_type == 'C':
            print(decrypt_caesar(text))
        elif encrypt_type == 'V':
            passkey = input("Passkey? ")
            print(decrypt_vigenere(text, passkey))
        else:
            num_rails = int(input("Number of rails? "))
            print(decrypt_railfence(text, num_rails))



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
