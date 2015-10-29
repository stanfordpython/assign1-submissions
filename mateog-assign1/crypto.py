"""
Assignment 1: Cryptography
Course: CS 92SI
Name: Mateo Garcia
Date: 2015-10-11

Encrypts and decrypts Caesar, Vigenere, and Railfence ciphers.
"""

import math

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def encrypt_caesar(plaintext):
        """
        Encrypts plaintext using a Caesar cipher. Maps alphabet to cipher
        alphabet shifted by three characters to the left, such that A maps to D, etc.
        Converts plaintext to list, and finds ciphertext version of each
        character using map.
        """
        encrypt_alphabet = alphabet[3:] + alphabet[:3]
        print(encrypt_alphabet)
        encrypt_map = {}
        for i in range (0, 26):
                encrypt_map[alphabet[i]] = encrypt_alphabet[i]

        plaintext = plaintext.upper()
        ciphertext = list(plaintext)
        for i in range(0, len(plaintext)):
            ciphertext[i] = encrypt_map[ciphertext[i]]

        return "".join(ciphertext)


def decrypt_caesar(ciphertext):
        """
        Decrypts a ciphertext using a Caesar cipher. Maps alphabet to plaintext
        alphabet shifted by three characters to the right, such that A maps to X, etc.
        Converts ciphertext to list, and finds plaintext version of each
        character using map.
        """
        encrypt_alphabet = alphabet[-3:] + alphabet[:-3]
        print(encrypt_alphabet)
        encrypt_map = {}
        for i in range (0, 26):
                encrypt_map[alphabet[i]] = encrypt_alphabet[i]

        ciphertext = ciphertext.upper()
        plaintext = list(ciphertext)
        for i in range(0, len(ciphertext)):
            plaintext[i] = encrypt_map[plaintext[i]]

        return "".join(plaintext)


def encrypt_vigenere(plaintext, keyword):
        """
        Encrypts plaintext using a Vigenere cipher with a keyword. Creates
        ciphertext list of same length as plaintext, gets ASCII value of
        each letter in plaintext and corresponding letter in keyword, subtracts
        value of 'A', adds key character value to plaintext value, mods sum by
        26 to get a wrapping shift, and adds 'A' back to sum before getting ASCII
        character back from ciphertext value.
        """
        plaintext = plaintext.upper()
        keyword = keyword.upper()
        ciphertext = list(plaintext)
        for i in range(0, len(plaintext)):
            p = ord(plaintext[i]) - ord('A')
            k = ord(keyword[i % len(keyword)]) - ord('A')
            ciphertext[i] = chr(((p + k) % 26) + ord('A'))

        return "".join(ciphertext)


def decrypt_vigenere(ciphertext, keyword):
        """
        Decrypts ciphertext using a Vigenere cipher with a keyword. Creates
        plaintext list of same length as ciphertext, gets ASCII value of
        each letter in ciphertext and corresponding letter in keyword, subtracts
        value of 'A' from each, subtracts key character value from ciphertext value,
        mods sum by 26 to get a wrapping shift, and adds 'A' back to sum before
        getting ASCII character back from plaintext value.
        """
        ciphertext = ciphertext.upper()
        keyword = keyword.upper()
        plaintext = list(ciphertext)
        for i in range(0, len(ciphertext)):
            p = ord(ciphertext[i]) - ord('A')
            k = ord(keyword[i % len(keyword)]) - ord('A')
            plaintext[i] = chr(((p - k) % 26) + ord('A'))

        return "".join(plaintext)


def encrypt_railfence(plaintext, num_rails):
        """
        Encrypts plaintext using a railfence cipher. Sets plaintext to uppercase,
        and loops through each character in plaintext to determine its rail. First
        splits characters into fragments, which include the character at a peak/trough
        (inclusive) through the character at the next peak/trough (exclusive). Next,
        determines whether fragment is descending or ascending, and splits characters
        from the start of the fragment to the end into their corresponding rail of
        increasing index, or the opposite, respectively.
        """
        plaintext = plaintext.upper()
        frag_len = num_rails - 1
        rails = [""] * num_rails
        for i in range(0, len(plaintext)):
            frag_num = int(i / frag_len)
            if frag_num % 2 == 0:
                rails[i % frag_len] += plaintext[i]
            else:
                rails[-(1 + i % frag_len)] += plaintext[i]

        ciphertext = ""
        for r in rails:
            ciphertext += r

        return ciphertext


def decrypt_railfence(ciphertext, num_rails):
        """
        Encrypts plaintext using a railfence cipher.
        Add more implementation details here.
        """
        ciphertext = ciphertext.upper()
        frag_len = num_rails - 1
        rails = [""] * num_rails
        num_full_frags = int(len(ciphertext) / frag_len)
        len_last_frag = len(ciphertext) % frag_len
        for i in range(0, num_rails):

            # TOP RAIL
            if i == 0:
                num_peaks = int(num_full_frags / 2)
                if num_full_frags % 2 != 0 or len_last_frag > 0: # If extra letter from full/part fragment
                    num_peaks += 1
                rails[i] = ['-'] * num_peaks

            # BOTTOM RAIL
            elif i == num_rails - 1:
                num_troughs = int(num_full_frags / 2)
                if num_full_frags % 2 != 0 and len_last_frag > 0: # If extra letter from full/part fragment
                    num_troughs += 1
                rails[i] = ['-'] * num_troughs

            # MIDDLE RAILS
            else:
                num_chars = num_full_frags
                if num_full_frags % 2 == 0 and len_last_frag > i: # same  as ^^
                    num_chars += 1
                elif num_full_frags % 2 != 0 and num_rails - len_last_frag <= i: # same  as ^^
                    num_chars += 1
                rails[i] = ['-'] * num_chars

        # CONSTRUCT RAILS
        spacing = frag_len * 2
        for i in range(0, num_rails):
            if i == 0 or i == num_rails - 1:
                rails[i] = ciphertext[::spacing]
            else:
                rails[i][::2] = ciphertext[::spacing]
                odd_index_char_start = i + ((frag_len - i) * 2)
                rails[i][1::2] = ciphertext[odd_index_char_start::spacing]

        # CONSTRUCT FRAGMENTS
        num_frags = num_full_frags
        if num_full_frags > 0:
            num_frags += 1
        frags = [""] * num_frags
        for i in range(0, num_frags):
            startIndex = i * frag_len
            frags[i] = ciphertext[startIndex:startIndex + frag_len]

        # CONVERT TO PLAINTEXT
        plaintext = list(ciphertext)
        for i in range(0, len(ciphertext)):
            frag_num = int(i / frag_len)
            if frag_num % 2 == 0:
                plaintext[i] = rails[i % frag_len][0]
                rails[i % frag_len] = rails[i % frag_len][1:]
            else:
                plaintext[i] = rails[-(1 + i % frag_len)][0]
                rails[-(1 + i % frag_len)] = rails[-(1 + i % frag_len)][1:]

        return "".join(plaintext)

def read_from_file(filename):
        """
        Reads and returns content from a file.
        Add more implementation details here.
        """
        text = ""
        with open(filename, 'r') as f:
            text = f.read()

        return text


def write_to_file(filename, content):
        """
        Writes content to a file.
        Add more implementation details here.
        """
        with open(filename, 'w') as f:
            f.write(content)


def clean_up_text(text):
        text = text.upper()
        text = list(text)
        i = 0
        while i < len(text):
            if not text[i].isalpha():
                text.remove(text[i])
            else:
                i += 1
        return "".join(text)


def run_suite():
        """
        Runs a single iteration of the cryptography suite.

        Asks the user for input text from a string or file, whether to encrypt
        or decrypt, what tool to use, and where to show the output.

        Assumes filenames are valid.
        """

        # INPUT
        print("*Input*")
        choice = input("(F)ile or (S)tring? ").upper()
        while not choice or choice[0] not in ['F', 'S']:
            choice = input("Please enter either 'F' or 'S'. (F)ile or (S)tring? ").upper()

        text = ""
        if choice == 'F':
            filename = input("Filename? ")
            text = read_from_file(filename)
            text = clean_up_text(text)
        else:
            text = input("Enter the string to encrypt: ")
            text = clean_up_text(text)

        # TRANSFORM
        print("*Transform*")
        choice = input("(E)ncrypt or (D)ecrypt? ").upper()
        while not choice or choice[0] not in ['E', 'D']:
            choice = input("Please enter either 'E' or 'D'. (E)ncrypt or (D)ecrypt? ").upper()
        encrypt = choice == 'E'

        choice = input("(C)aesar, (V)igenere, or (R)ailfence? ").upper()
        while not choice or choice[0] not in ['C', 'V', 'R']:
            choice = input("Please enter either 'C', 'V', or 'R'. (C)aesar, (V)igenere, or (R)ailfence? ").upper()

        # CIPHER TYPE
        result = ""
        if choice == 'C':
            if encrypt:
                result = encrypt_caesar(text)
            else:
                result = decrypt_caesar(text)
        elif choice == 'V':
            keyword = input("Passkey? ")
            if encrypt:
                result = encrypt_vigenere(text, keyword)
            else:
                result = decrypt_vigenere(text, keyword)
        else:
            num_rails = input("Number of rails? ")
            while not num_rails.isdigit():
                num_rails = input("Please enter a valid number. Number of rails? ")
            num_rails = int(num_rails)
            if encrypt:
                result = encrypt_railfence(text, num_rails)
            else:
                result = decrypt_railfence(text, num_rails)

        # OUTPUT
        print("*Output*")
        choice = input("(F)ile or (S)tring? ").upper()
        while not choice or choice[0] not in ['F', 'S']:
            choice = input("Please enter either 'F' or 'S'. (F)ile or (S)tring? ").upper()

        if choice == 'F':
            filename = input("Filename? ")
            print("Writing ciphertext to", filename, "...")
            write_to_file(filename, result)
        else:
            print("The plaintext is: ", result)


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
