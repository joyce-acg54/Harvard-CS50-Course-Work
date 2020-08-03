from cs50 import get_float, get_string
from sys import argv


def main():

    # give proper command line argument: 2 arguments, 2nd argument must be positive
    if len(argv) != 2:
        print("ERROR: Provide 2 command-line arguments!")
        exit(1)

    k = int(argv[1])
    if k < 1:
        print("ERROR: Positive 2nd command-line argument!")

    # prompt to give plain text and output cipher
    plaintext = get_string("plaintext: ")
    print("ciphertext: ", end="")

    # convert each char of plaintext to ascii
    for c in plaintext:

        # if not alphabetical
        if not c.isalpha():
            print(c, end="")
            continue  # moves on to the next part of the loop

        # if c is lower give value 65 otherwise, give value 97
        offset = 65 if c.isupper() else 97

        pi = ord(c) - offset
        ci = (pi + k) % 26

        print(chr(ci + offset), end="")
    print()


if __name__ == "__main__":
    main()