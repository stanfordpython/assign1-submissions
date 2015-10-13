"""
Assignment 1: Cryptography
Course: CS 92SI
Name: Alan Deng
Date: Oct 9, 2015

Cryptography suite implementing the Caesar, Vigenere, and Railfence ciphers
to encrypt or decrypt user supplied input strings from a file or the terminal,
along with secondary parameters specific to each method. User also specifies
whether the output is written to file or displayed on terminal.
"""

def encrypt_caesar(plaintext, shift):
    """
    Encrypts plaintext using a Caesar cipher with a default shift of 3.
    User can override with alternative value to shift, taken mod 26. 
    Assumes input plaintext consists of capitalized alphabetical string.
    If shifted index goes beyond 'Z', wraps back around to the beginning
    """
    shift = shift % 26
    output = [chr(ord(letter) + shift) for letter in plaintext]
    for i in range(len(output)):
        if ord(output[i]) > ord("Z"): #index out of range
            output[i] = chr(ord(output[i]) - 26)
    return "".join(output)

def decrypt_caesar(ciphertext, shift):
    """
    Decrypts ciphertext using a Caesar cipher with a default shift of 3.
    User can override with alternative value to shift, taken mod 26. 
    Assumes input ciphertext consists of capitalized alphabetical string.
    If shifted index goes below 'A', wraps back around to the end
    """
    shift = shift % 26
    output = [chr(ord(letter) - shift) for letter in ciphertext]
    for i in range(len(output)):
        if ord(output[i]) < ord("A"): #index out of range
            output[i] = chr(ord(output[i]) + 26)
    return "".join(output)

def encrypt_vigenere(plaintext, keyword):
    """
    Encrypts plaintext using a Vigenere cipher with a keyword.
    Assumes plaintext and keyword are both capitalized alphabetical strings.
    If shifted index goes beyond 'Z', wraps back around to the beginning
    """
    keyphrase = keyword * (len(plaintext) // len(keyword) + 1) #repeat keyword
    output = [chr(ord(x) + ord(y) - 65) for (x,y) in zip(plaintext, keyphrase)] #cap letters start at 64
    for i in range(len(output)):
        if ord(output[i]) > ord("Z"): #index out of range
            output[i] = chr(ord(output[i]) - 26)
    return "".join(output)

def decrypt_vigenere(ciphertext, keyword):
    """
    Decrypts ciphertext using a Vigenere cipher with a keyword.
    Assumes ciphertext and keyword are both capitalized alphabetical strings.
    If shifted index goes below 'A', wraps back around to the end
    """
    keyphrase = keyword * (len(ciphertext) // len(keyword) + 1) #repeat keyword
    output = [chr(ord(x) - ord(y) + 65) for (x,y) in zip(ciphertext, keyphrase)]
    for i in range(len(output)):
        if ord(output[i]) < ord("A"): #index out of range
            output[i] = chr(ord(output[i]) + 26)
    return "".join(output)

def encrypt_railfence(plaintext, num_rails):
    """
    Encrypts plaintext using a railfence cipher with a given number of rails.
    The first and last rails only have elements spaced evenly apart.
    The other rails in between have a secondary component going back up, 
    which is alternately spliced with this rail to generate the complete rail. 
    If the number of rails is 1, the plaintext is returned as the ciphertext.
    """
    if num_rails == 1:
        return(plaintext)
    output = []
    for i in range(num_rails):
        down_rail = plaintext[i::2*(num_rails - 1)]
        if (i in range (1, num_rails - 1)):
            up_rail = plaintext[(2*(num_rails-1)-i)::2*(num_rails - 1)]
            output_string = ["".join(x) for x in zip(down_rail, up_rail)]
            if len(down_rail) > len(up_rail):
                output_string.append(down_rail[-1])
            output.append("".join(output_string))
        else:
            output.append(down_rail)
    return "".join(output)

def decrypt_railfence(ciphertext, num_rails):
    """
    Decrypts ciphertext using a railfence cipher with a given number of rails.
    A dummy plaintext is created initially with the same length as the ciphertext, 
    which is iteratively replaced by elements from the rails formed from relevant
    slices of the ciphertext. A counter starting from 0 advances to keep track of
    which rail we are currently on. The first and last rail only deal with a single
    rail, the internal rails are further split into the pieces going down and up.
    If the number of rails is 1, the ciphertext is returned as the plaintext.
    """
    if num_rails == 1:
        return(ciphertext)
    output = len(ciphertext)*['-']
    curr = 0
    for i in range(num_rails):
        rail = (len(ciphertext)-1-i)//(2*(num_rails-1)) + 1
        if (i in range(1, num_rails-1)):
            rail2 = (len(ciphertext)-1+i)//(2*(num_rails-1))
            section = ciphertext[curr:(curr+rail+rail2)]
            output[i::2*(num_rails-1)] = section[::2]
            output[2*(num_rails-1)-i::2*(num_rails-1)] = section[1::2]
            curr += rail + rail2
        else:
            output[i::2*(num_rails-1)] = ciphertext[curr:(curr+rail)]
            curr += rail
    return "".join(output)

def read_from_file(filename):
    """
    Reads and returns content from a file.
    Strips away non-alphanumerical characters and converts letters to uppercase.
    """
    with open(filename, 'r') as f:
        content = f.read()
    return "".join([x.upper() for x in content if x.isalnum()])

def write_to_file(filename, content):
    """
    Writes content to a file. Spacing, punctuation, and casing will be lost.
    Replaces contents if filename exists, otherwise creates new file for it.
    """
    with open(filename, 'w') as f:
        f.write(content)

def run_suite():
    """
    Runs a single iteration of the cryptography suite.
    Asks the user for input text from a string or file, whether to encrypt
    or decrypt, what tool to use, and where to show the output.

    Depending on the input, further prompts will get the relevant parameters,
    (e.g. shift for Caesar, passkey for Vigenere, number of rails for Railfence)
    Primary prompts requires only the first letter to match choice, reprompting
    if not the case. This robustness is not extended to these secondary prompts.
    Input strings are stripped to alphanumerical characters and converted to uppercase.
    """
    input_dict = {"F":"File", "S":"String", "D":"Decrypting", "E":"Encrypting", "C":"Caesar", "V":"Vigenere", "R":"Railfence"}

    print("*Input*")
    format = input("(F)ile or (S)tring? ").upper()
    while not format or format[0] not in ['F', 'S']:
        format = input("Please enter either 'F' for file or 'S' for string: ").upper()
    if format[0] == "F":
        filename = input("Filename? ")
        input_text = read_from_file(filename)
    else:
        raw_string = input("Enter the string to encrypt: ")
        input_text = "".join([x.upper() for x in raw_string if x.isalnum()])

    print("*Transform*")
    operation = input("(E)ncrypt or (D)ecrypt? ").upper()
    while not operation or operation[0] not in ['E', 'D']:
        operation = input("Please enter either 'E' for encrypt or 'D' for decrypt: ").upper()
    cipher = input("(C)aesar, (V)igenere, or (R)ailfence? ").upper()
    while not cipher or cipher[0] not in ['C','V','R']:
        cipher = input("Please enter either 'C' for Caesar, 'V' for Vigenere, or 'R' for Railfence: ").upper()
    if cipher[0] == "C":
        shift = input("Shift? (Default is 3): ")
        if not shift:
            shift = "3"
    elif cipher[0] == "V":
        passkey = input("Passkey? ").upper()
    else:
        num_rails = input("Number of rails? ")

    print_list = []
    print_list.append(input_dict[operation[0]])
    if format == "F":
        print_list.append("the contents of")
        print_list.append(filename)
    else:
        print_list.append(input_text)
    print_list.append("using")
    print_list.append(input_dict[cipher[0]])
    print_list.append("cipher with")
    if cipher[0] == "C":
        print_list.append("shift of")
        print_list.append(shift)
    elif cipher[0] == "V":
        print_list.append("key")
        print_list.append(passkey)
    else:
        print_list.append(num_rails)
        print_list.append("rails")
    print_list.append("...")
    print(" ".join(print_list))

    print("*Output*")
    out_format = input("(F)ile or (S)tring? ").upper()
    while not out_format or out_format[0] not in ['F', 'S']:
        out_format = input("Please enter either 'F' for file or 'S' for string: ").upper()
    result = []
    if operation[0] == "E":
        if cipher[0] == "C":
            result = encrypt_caesar(input_text,int(shift))
        elif cipher[0] == "V":
            result = encrypt_vigenere(input_text,passkey)
        else:
            result = encrypt_railfence(input_text,int(num_rails))
    else:
        if cipher[0] == "C":
            result = decrypt_caesar(input_text,int(shift))
        elif cipher[0] == "V":
            result = decrypt_vigenere(input_text,passkey)
        else:
            result = decrypt_railfence(input_text,int(num_rails))
    if out_format[0] == "S":
        if operation[0] == "E":
            print("The ciphertext is: " + result)
        else:
            print("The plaintext is: " + result)
    else:
        out_file = input("Filename? ")
        write_to_file(out_file, result)
        if operation[0] == "E":
            print("Writing ciphertext to " + out_file + " ...")
        else:
            print("Writing plaintext to " + out_file + " ...")

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