"""
Assignment 1: Cryptography
Course: CS 92SI
Name: Harper Carroll
Date: 10/9/15

An interactive ciphering and deciphering program. Allows the user to encipher or decipher
either a string or a file using one of three methods: a caesar cipher, a de Vigenere cipher,
and a railfence cipher (well, it should... not really with my implementation because I didn't have time).
Then, the user can receive the encrypted or decrypted message via a printed string or a
file.

"""

alphabet_upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alphabet_lower = "abcdefghijklmnopqrstuvwxyz"

def encrypt_caesar(plaintext):
    """
    Encrypts plaintext using a Caesar cipher of a shift of 3.
    """
    ciphertext = ""
    for letter in plaintext:
        if (letter in alphabet_lower):
            newLetter = alphabet_lower.index(letter) + 3
            newLetter = newLetter % 26
            ciphertext += alphabet_lower[newLetter]
        else:
            newLetter = alphabet_upper.index(letter) + 3
            newLetter = newLetter % 26
            ciphertext += alphabet_upper[newLetter]

    print("Encrypting " + plaintext + " using Caesar cipher...")
    return ciphertext;

def decrypt_caesar(ciphertext):
    """
    Decrypts a ciphertext using a Caesar cipher of a shift of 3.
    """
    plaintext = ""
    for letter in ciphertext:
        if (letter in alphabet_lower):
            newLetter = alphabet_lower.index(letter) - 3
            if (newLetter < 0):
                newLetter = 26 + newLetter;
            else:
                newLetter = newLetter % 26
            plaintext += alphabet_lower[newLetter]
        else:
            newLetter = alphabet_upper.index(letter) - 3
            if (newLetter < 0):
                newLetter = 26 + newLetter;
            else:
                newLetter = newLetter % 26
            plaintext += alphabet_upper[newLetter]
    print("Decrypting " + ciphertext + " using Caesar cipher...")
    return plaintext;

def encrypt_vigenere(plaintext, keyword):
    """
    Encrypts plaintext using a Vigenere cipher with a keyword.
    """
    ciphertext = ""
    for index, letter in enumerate(plaintext):
        if (index > (len(keyword) - 1)):
            index = index % len(keyword)
        if (letter in alphabet_lower):
            newLetter = alphabet_lower.index(letter) + alphabet_upper.index(keyword[index])
            newLetter = newLetter % 26
            ciphertext += alphabet_lower[newLetter]
        else:
            newLetter = alphabet_upper.index(letter) + alphabet_upper.index(keyword[index])
            newLetter = newLetter % 26
            ciphertext += alphabet_upper[newLetter]

    print("Encrypting " + plaintext + " using Vigenere cipher with key " + keyword + "...")
    return ciphertext;


def decrypt_vigenere(ciphertext, keyword):
    """
    Decrypts ciphertext using a Vigenere cipher with a keyword.
    """
    plaintext = ""
    for index, letter in enumerate(ciphertext):
        if (index > (len(keyword) - 1)):
            index = index % len(keyword)
        if (letter in alphabet_lower):
            newLetter = alphabet_lower.index(letter) - alphabet_upper.index(keyword[index])
            if (newLetter < 0):
                newLetter = 26 + newLetter;
            else:
                newLetter = newLetter % 26
            plaintext += alphabet_lower[newLetter]
        else:
            newLetter = alphabet_upper.index(letter) - alphabet_upper.index(keyword[index])
            if (newLetter < 0):
                newLetter = 26 + newLetter;
            else:
                newLetter = newLetter % 26
            plaintext += alphabet_upper[newLetter]

    print("Decrypting " + ciphertext + " using Vigenere cipher with key " + keyword + "...")
    return plaintext;

def encrypt_railfence(plaintext, num_rails):
    """
    Encrypts plaintext using a railfence cipher.
    """
    l = []
    for letter in plaintext:
        l.append(letter)
    used_indices = []
    distance = 2 * (num_rails - 1)
    currentRailIndices = []
    currentRailIndices.append([])
    currentRailIndices.append([])
    indices = list(range(0, len(plaintext)))
    rail = 1
    while (rail <= num_rails):
        for i in indices[(rail-1)::distance]:
            if (i not in used_indices):
                used_indices.append(i)
                currentRailIndices.append(i)
        for j in indices[(2*(rail-1))::distance]:
            if (j not in used_indices):
                used_indices.append(j)
                currentRailIndices[rail-1].append(j)
        currentRailIndices[rail-1] = sorted(currentRailIndices[rail-1])
        rail += 1

    ciphertext = ""
    for i in range(num_rails):
        for j in range((len(plaintext)/3 + len(plaintext%3))):
            ciphertext += plaintext[currentRailIndices[i][j]]

    print("Encrypting " + plaintext + " using Railfence cipher with " + str(num_rails) + " rails...")
    return ciphertext

def decrypt_railfence(ciphertext, num_rails):
    """
    Encrypts plaintext using a railfence cipher.
    Add more implementation details here.
    """
    pass  # Your implementation here


def read_from_file(filename):
    """
    Reads and returns content from a file.
    Add more implementation details here.
    """
    with open(filename, 'r') as f:
        content = f.read()
    f.close()
    return content;

def write_to_file(filename, content):
    """
    Writes content to a file.
    Add more implementation details here.
    """
    with open(filename, 'w+') as f:
        f.write(content)
    f.close()
    return f;


def run_suite():
    """
    Runs a single iteration of the cryptography suite.

    Asks the user for input text from a string or file, whether to encrypt
    or decrypt, what tool to use, and where to show the output.
    """
    print("*Input*")
    input_combination = ""
    file_or_string = input("(F)ile or (S)tring? ")
    string = ""
    content = ""
    while (file_or_string.upper()[0] not in ['S', 'F']):
        print ("Invalid response.")
        file_or_string = input("(F)ile or (S)tring? ")
    if (file_or_string.upper()[0] == 'F'):
        filename = input("Filename: ")
        roughContent = read_from_file(filename)
        for letter in roughContent: #eliminates all non-alphabetical characters
            if (letter.isalpha()):
                content += letter
    elif (file_or_string.upper()[0] == 'S'):
         roughString = input("Enter the string to transform: ")
         string = ""
         for letter in roughString: #eliminates all non-alphabetical characters
            if (letter.isalpha()):
                string += letter

    input_combination += file_or_string.upper()[0]

    print("*Transform*")
    encrypt_or_decrypt = input("(E)ncrypt or (D)ecrypt? ")
    while (encrypt_or_decrypt.upper()[0] not in ['E', 'D']):
        print ("Invalid response.")
        file_or_string = input("(E)ncrypt or (D)ecrypt?")
    input_combination += encrypt_or_decrypt.upper()[0]

    tool = input("(C)aesar, (V)igenere, or (R)ailfence? ")
    while (tool.upper()[0] not in ['C', 'V', 'R']):
        print ("Invalid response.")
        tool = input("(C)aesar, (V)igenere, or (R)ailfence?")
    input_combination += tool.upper()[0]
    transformed = ""

    if (input_combination[0] == 'F'): #if file
        if (input_combination[1] == 'E'): #encrypt
            if (input_combination[2] == 'C'): #caesar
                transformed = encrypt_caesar(content)
            elif (input_combination[2] == 'V'): #de vigenere
                keyword = input("Keyword? ")
                keyword = keyword.upper()
                transformed = encrypt_vigenere(content, keyword)
            else: #if railfence
                num_rails = int(input("Number of rails? "))
                transformed = encrypt_railfence(content, num_rails)
        else: #decrypt
            if (input_combination[2] =='C'):
                transformed = decrypt_caesar(content)
            elif (input_combination[2] == 'V'): #de vigenere
                keyword = input("Keyword? ")
                keyword = keyword.upper()
                transformed = decrypt_vigenere(content, keyword)
            else: #if railfence
                num_rails = int(input("Number of rails? "))
                transformed = decrypt_railfence(content, num_rails)

    else: #if string
        if (input_combination[1] == 'E'): #encrypt
            if (input_combination[2] == 'C'): #caesar
                transformed = encrypt_caesar(string)
            elif (input_combination[2] == 'V'): #de vigenere
                keyword = input("Keyword? ")
                keyword = keyword.upper()
                transformed = encrypt_vigenere(string, keyword)
            else: #if railfence
                num_rails = int(input("Number of rails? "))
                transformed = encrypt_railfence(string, num_rails)
        else: #decrypt
            if (input_combination[2] =='C'):
                transformed = decrypt_caesar(string)
            elif (input_combination[2] == 'V'): #de vigenere
                keyword = input("Keyword? ")
                keyword = keyword.upper()
                transformed = decrypt_vigenere(string, keyword)
            else: #if railfence
                num_rails = int(input("Number of rails? "))
                transformed = decrypt_railfence(string, num_rails)
    print("")



    print("*Output*")
    file_or_string = input("(F)ile or (S)tring? ")
    while (file_or_string.upper()[0] not in ['S', 'F']):
        print ("Invalid response.")
        file_or_string = input("(F)ile or (S)tring? ")
    if (file_or_string.upper()[0] == 'F'):
        filename = input("Filename? ")
        print("Writing transformed text to " + filename + "...")
        file_of_content = write_to_file(filename, content)
    elif (file_or_string.upper()[0] == 'S'):
        print("The transformed text is: " + transformed)


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
