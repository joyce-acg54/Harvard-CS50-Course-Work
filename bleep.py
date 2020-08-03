from cs50 import get_string
from sys import argv


def main():
    # ensure proper usage of command-line
    if len(argv) != 2:
        print("USAGE: python bleep.py banned.txt")
        exit(1)

    # open file indicated in argument [1]
    file = open(argv[1])
    # create arbitrary set
    banned = set()
    # adds words from file to set
    for line in file:
        banned.add(line.strip().lower())

    # prompt user for a message
    inputString = get_string("Enter a message: ")
    # output nothing
    outputString = ""
    # create list words with input message of user splitted into words with space ()
    words = inputString.split()

    # iterate over all words in words
    for word in words:

        # lowercase all characters in word and find in banned, if it's there, output *
        if word.lower() in banned:
            outputString += "*" * len(word) + " "
        # otherwise, just output the word
        else:
            outputString += word + " "

    print(outputString.strip())


if __name__ == "__main__":
    main()
