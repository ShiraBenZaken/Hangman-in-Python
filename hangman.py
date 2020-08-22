'''
 Final exercise-> Python programming course 
 shira ben zaken
 07/07/2020
  Exercise:
    1. The program gets from the player:
        a. a text file path; The text file contains English word list separated by spaces
        b. an index
    2. The player will get the status of his progress in the game:
            (1) hangman
            (2) the secret word
    3. Check weather the input is valid = an English letter that was not guessed previously
            (1)  if the input is invalid print 'X' and repeat 3.B.
            (2)  If the input is valid and incorrect - print ':(', increment number of tries and repeat 3.A.
            (3)  If the input is valid and correct - check if the player guessed all the word

 My addtions:
    (1) The output coloring scheme:
        RED = Wrong input;
        GREEN = Hidden secret word;
        CYAN = Hangman image;            
        Blue = final result;
        - MAGENTA = DEBUG
    (2)  an empty input for the index means a radom index
'''
# import standard libraries functions
import random
import os

from colorama import init
from termcolor import colored

COLOR_CODE = {
    "INSTRUCTIONS": 'yellow',
    "INVALID_INPUT": 'red',  # ('red',['bold']),
    "WORD": 'green',
    "HANGMAN": 'cyan',  # ('cyan',['bold']),
    "WELCOME": 'blue',
    "RESULT": 'blue',  # ('blue',['bold']),
    "DEBUG": 'magenta'}

DEBUG_LOGGING = False
DEFAULT_DICTIONARY = "dictionary.txt"
WELCOME_SCREEN_FILE = "welcome_screen.txt"


def print_debug(message):
    if DEBUG_LOGGING:
        print(colored(message, COLOR_CODE["DEBUG"]))


def print_err_input(message):
    print(colored(message, COLOR_CODE["INVALID_INPUT"]))


def main():
    # main-> welcome screen
    with open(WELCOME_SCREEN_FILE, 'r') as welcome_file:
        print(colored(welcome_file.read(), COLOR_CODE["WELCOME"]))

    # constants
    MAX_TRIES = 7

    # a text file path; The text file contains English word list separated by spaces
    text_file_path = input("Enter file path: ")
    # index
    index_str = input("Enter index: ")
    #  an empty input for the index means a random index
    try:
        secret_word_index = int(index_str)
    except:
        secret_word_index = random.randint(1, 1000000)
    print_debug("1. Process input = {0} {1}".format(text_file_path, secret_word_index))

    # 2.  the secret word..
    try:
        secret_word = choose_word(text_file_path, secret_word_index)[1]
    except:
        try:
            text_file_path = DEFAULT_DICTIONARY
            secret_word = choose_word(text_file_path, secret_word_index)[1]
        except:
            print_err_input("Couldn't choose_word from {0} index {1}".format(text_file_path, secret_word_index))
    print_debug("2. Generate secret = {0}".format(secret_word))

    # 3. Hangman game starts
    old_letters_guessed = list()
    print(colored("Let's start!", COLOR_CODE["WELCOME"]))
    # main steps loop
    numOfTries = 1

    while numOfTries <= MAX_TRIES:
        # status in the program
        hangman_picture = print_hangman(numOfTries)
        print(colored(hangman_picture, COLOR_CODE["HANGMAN"]))
        if numOfTries == MAX_TRIES:
            print_debug("Lose condition met {0} = {1}.format(numOfTries, MAX_TRIES)")
            # print 'LOST' and exit
            print(colored("LOST", COLOR_CODE["RESULT"]))
            break
        hidden_word = show_hidden_word(secret_word, old_letters_guessed)
        print(colored(hidden_word, COLOR_CODE["WORD"]))
        if check_win(secret_word, old_letters_guessed):
            print_debug("Win condition met - all secret word letters guessed")
            # print 'WON' and exit
            print(colored("WON", COLOR_CODE["RESULT"]))
            break

        while True:
            guess_letter_input = input("Guess a letter:")
            # Check weather the input is valid
            is_valid = try_update_letter_guessed(guess_letter_input, old_letters_guessed)
            if not is_valid:
                print(colored("X", COLOR_CODE["INVALID_INPUT"]))
                continue
            elif guess_letter_input.lower() not in secret_word.lower():
                print(colored(":(", COLOR_CODE["INVALID_INPUT"]))
                numOfTries += 1
                print_debug("MISS! tries {0}/{1}. Continue guessing".format(numOfTries, MAX_TRIES))
                break
            else:
                print_debug("BULLZIE! Continue guessing")
                break

    # before exit - print the secret word (for those who missed it)
    print(colored("The word was {0}".format(secret_word), COLOR_CODE["RESULT"]))

# Run main
if (__name__ == "__main__"):
    init()
    main()

#ex1
def check_valid_input(input_string, old_letter_guessed):
    # validation

    is_alpha = input_string.isalpha()
    is_single = (len(input_string) == 1)
    lowered_input = input_string.lower()
    if (is_alpha) and not (is_single):
        return False
    elif not (is_alpha) and (is_single):
        return False
    elif not (is_alpha) and not (is_single):
        return False
    elif lowered_input in old_letter_guessed:
        return False
    else:  # (is_alpha) and (is_single) + not guessed earlier
        return True

#ex2
def try_update_letter_guessed(input_string, old_letter_guessed):
    # update letter_guessed list if input is valid (see is_valid_letter_input)

    lowered_input = input_string.lower()
    if check_valid_input(lowered_input, old_letter_guessed):
        old_letter_guessed += lowered_input
        return True
    else:
        return False
#ex3
def show_hidden_word(secret_word, letters_guessed):
#show if the chare is same...
    out_str = ""
    for secret_char in secret_word:
        if secret_char.lower() in letters_guessed:
            out_str += secret_char + " "
        else:
            out_str += "_ "
    return out_str


def check_win(secret_word, letters_guessed):
    #check in win case..
    for secret_char in secret_word:
        if not secret_char.lower() in letters_guessed:
            return False
    # all secret_chars were guessed
    return True

#ex4
from termcolor import colored

HANGMAN_PHOTOS = {
    1: ["x-------x"],
    2: ["x-------x",
        "|        ",
        "|        ",
        "|        ",
        "|        ",
        "|        "],
    3: ["x-------x",
        "|       |",
        "|       0",
        "|        ",
        "|        ",
        "|        "],
    4: ["x-------x",
        "|       |",
        "|       0",
        "|       |",
        "|        ",
        "|        "],
    5: ["x-------x",
        "|       |",
        "|       0",
        "|      /|\\",
        "|        ",
        "|        "],
    6: ["x-------x",
        "|       |",
        "|       0",
        "|      /|\\",
        "|      / ",
        "|        "],
    7: ["x-------x",
        "|       |",
        "|       0",
        "|      /|\\",
        "|      / \\",
        "|        "]}


def print_hangman(num_of_tries, color='white'):
    """
    hangman picture..
    """
    output = ""
    for line in HANGMAN_PHOTOS[num_of_tries]:
        output += line + "\n"
    return output

#ex5
def choose_word(file_name, n_):

    # use a map's key uniqueness to count only unique words
    word_map = {}

    # open the text file
    with open(file_name, 'r') as input_file:
        word_list = input_file.read().split()
        for word in word_list:
            word_map[word] = 0
    unique_word_list = list(word_map.keys())
    index = (n_ - 1) % len(word_list)
    # return the requested word
    return len(unique_word_list), word_list[index]